#!/usr/bin/env python3
import argparse
import datetime as dt
import json
import re
from pathlib import Path


CODEX_HOME = Path.home() / ".codex"
INDEX_PATH = CODEX_HOME / "session_index.jsonl"
SESSIONS_DIR = CODEX_HOME / "sessions"
ARCHIVED_DIR = CODEX_HOME / "archived_sessions"
DEFAULT_OUTPUT_DIR = Path.home() / "Documents" / "AI Conversation Records"


def load_index():
    records = []
    if not INDEX_PATH.exists():
        return records
    with INDEX_PATH.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return records


def all_session_files():
    files = []
    if SESSIONS_DIR.exists():
        files.extend(SESSIONS_DIR.rglob("*.jsonl"))
    if ARCHIVED_DIR.exists():
        files.extend(ARCHIVED_DIR.glob("*.jsonl"))
    return files


def find_session_file(session_id):
    for path in all_session_files():
        if session_id in path.name:
            return path
    return None


def parse_time(value):
    if not value:
        return dt.datetime.min.replace(tzinfo=dt.timezone.utc)
    try:
        return dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return dt.datetime.min.replace(tzinfo=dt.timezone.utc)


def timestamp_for_filename(value):
    parsed = parse_time(value)
    if parsed == dt.datetime.min.replace(tzinfo=dt.timezone.utc):
        return "undated_000000"
    return parsed.astimezone(dt.timezone.utc).strftime("%Y-%m-%d_%H%M%S")


def slugify(value):
    value = re.sub(r"[^\w\u4e00-\u9fff.-]+", "-", value, flags=re.UNICODE)
    value = re.sub(r"-+", "-", value).strip("-._")
    return value[:80] or "codex-conversation"


def choose_record(args, index):
    if args.id:
        for record in index:
            if record.get("id") == args.id:
                return record
        return {"id": args.id, "thread_name": args.id, "updated_at": None}

    sorted_index = sorted(index, key=lambda item: parse_time(item.get("updated_at")), reverse=True)
    if args.query:
        query = args.query.casefold()
        matches = [
            record
            for record in sorted_index
            if query in record.get("thread_name", "").casefold()
            or query in record.get("id", "").casefold()
        ]
        if not matches:
            raise SystemExit(f"No indexed Codex conversation matched query: {args.query}")
        return matches[0]

    if args.latest:
        if not sorted_index:
            raise SystemExit("No indexed Codex conversations found.")
        return sorted_index[0]

    raise SystemExit("Choose --latest, --query, --id, or --list.")


def iter_message_text(content):
    if isinstance(content, str):
        if content.strip():
            yield content
        return
    if not isinstance(content, list):
        return
    for item in content:
        if not isinstance(item, dict):
            continue
        text = item.get("text") or item.get("input_text") or item.get("output_text")
        if text and text.strip():
            yield text


def should_skip_user_text(text):
    stripped = text.strip()
    skip_prefixes = (
        "<environment_context>",
        "<permissions instructions>",
        "<app-context>",
        "<collaboration_mode>",
        "<skills_instructions>",
        "<plugins_instructions>",
        "========= MEMORY_SUMMARY BEGINS =========",
    )
    return any(stripped.startswith(prefix) for prefix in skip_prefixes)


def extract_messages(path):
    messages = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            if event.get("type") != "response_item":
                continue
            payload = event.get("payload") or {}
            if payload.get("type") != "message":
                continue
            role = payload.get("role")
            if role not in {"user", "assistant"}:
                continue
            parts = []
            for text in iter_message_text(payload.get("content")):
                if role == "user" and should_skip_user_text(text):
                    continue
                parts.append(text.rstrip())
            body = "\n\n".join(parts).strip()
            if body:
                messages.append({
                    "timestamp": event.get("timestamp"),
                    "role": role,
                    "text": body,
                })
    return messages


def write_markdown(record, source_path, messages, output_dir):
    output_dir.mkdir(parents=True, exist_ok=True)
    title = record.get("thread_name") or record.get("id") or "Codex conversation"
    updated_at = record.get("updated_at") or ""
    short_id = (record.get("id") or "unknown")[:8]
    filename = f"{timestamp_for_filename(updated_at)}__{slugify(title)}__thread-{short_id}.md"
    output_path = output_dir / filename
    exported_at = dt.datetime.now(dt.timezone.utc).isoformat()

    lines = [
        "---",
        f'title: "{title.replace(chr(34), chr(39))}"',
        f'id: "{record.get("id", "")}"',
        f'updated_at: "{updated_at}"',
        f'exported_at: "{exported_at}"',
        f'source: "{source_path}"',
        "---",
        "",
        f"# {title}",
        "",
    ]
    for message in messages:
        heading = "User" if message["role"] == "user" else "Assistant"
        lines.append(f"## {heading}")
        if message.get("timestamp"):
            lines.append("")
            lines.append(f'`{message["timestamp"]}`')
        lines.append("")
        lines.append(message["text"])
        lines.append("")

    output_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return output_path


def list_threads(index, limit):
    sorted_index = sorted(index, key=lambda item: parse_time(item.get("updated_at")), reverse=True)
    for record in sorted_index[:limit]:
        print(f"{record.get('updated_at', '')}\t{record.get('id', '')}\t{record.get('thread_name', '')}")


def build_parser():
    parser = argparse.ArgumentParser(description="Export local Codex Desktop conversations to Markdown.")
    selector = parser.add_mutually_exclusive_group()
    selector.add_argument("--latest", action="store_true", help="Export the most recently updated indexed thread.")
    selector.add_argument("--query", help="Export the most recent indexed thread whose title or id contains this text.")
    selector.add_argument("--id", help="Export a specific thread id.")
    selector.add_argument("--list", action="store_true", help="List recent indexed threads.")
    parser.add_argument("--limit", type=int, default=30, help="Number of threads to show with --list.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR, help="Directory for Markdown exports.")
    return parser


def main():
    args = build_parser().parse_args()
    index = load_index()
    if args.list:
        list_threads(index, args.limit)
        return

    record = choose_record(args, index)
    source_path = find_session_file(record.get("id", ""))
    if not source_path:
        raise SystemExit(f"Could not find JSONL source file for thread id: {record.get('id')}")

    messages = extract_messages(source_path)
    if not messages:
        raise SystemExit(f"No visible user/assistant messages found in: {source_path}")

    print(write_markdown(record, source_path, messages, args.output_dir))


if __name__ == "__main__":
    main()

