# Codex Conversation Exporter

Export local Codex Desktop conversations on macOS to clean Markdown.

This is a small, friendly tool for people who want to keep, search, or share selected Codex conversations without copying the whole chat by hand.

**Mac only for now.** It reads Codex Desktop's local files under `~/.codex/`, which currently makes this a macOS-focused tool.

## Features

- List recent Codex conversations
- Export the latest conversation
- Export by title keyword
- Export by thread id
- Save clean Markdown
- Filter out system/developer prompts, tool calls, encrypted reasoning, and raw logs

## Install

```bash
git clone https://github.com/stereosurfer/Codex-conversation-exporter.git
cd Codex-conversation-exporter
python3 -m pip install -e .
```

## Use

```bash
codex-conversation-exporter --list
codex-conversation-exporter --latest
codex-conversation-exporter --query "project planning"
codex-conversation-exporter --id 01234567-89ab-cdef-0123-456789abcdef
```

By default, exports are saved to:

```text
~/Documents/AI Conversation Records/
```

File names use:

```text
YYYY-MM-DD_HHMMSS__thread-title__thread-shortid.md
```

## Privacy

This tool only reads local Codex Desktop files. It does not upload anything.

Please review exported Markdown before sharing it. The exporter filters internal records, but your conversations may still contain private information that you typed.

## Contributing

Contributions are welcome. Add a new output format, improve filtering, build a simple UI, support more platforms, or make the workflow smoother.

Keep it small, useful, and kind to people who just want their conversations back.

## License

Apache License 2.0.

---

# Codex 對話匯出器

把 macOS 上的 Codex Desktop 本機對話匯出成乾淨的 Markdown。

這是一個小而實用的工具，給想保存、搜尋或分享特定 Codex 對話的人，不用再手動一段一段複製。

**目前只支援 Mac。** 它讀取 Codex Desktop 在 `~/.codex/` 底下的本機檔案，所以目前定位是 macOS 工具。

## 功能

- 列出最近的 Codex 對話
- 匯出最新對話
- 用標題關鍵字匯出
- 用 thread id 匯出
- 輸出乾淨 Markdown
- 過濾 system/developer prompt、工具呼叫、加密推理與 raw logs

## 安裝

```bash
git clone https://github.com/stereosurfer/Codex-conversation-exporter.git
cd Codex-conversation-exporter
python3 -m pip install -e .
```

## 使用

```bash
codex-conversation-exporter --list
codex-conversation-exporter --latest
codex-conversation-exporter --query "專案規劃"
codex-conversation-exporter --id 01234567-89ab-cdef-0123-456789abcdef
```

預設匯出到：

```text
~/Documents/AI Conversation Records/
```

檔名規則：

```text
YYYY-MM-DD_HHMMSS__thread-title__thread-shortid.md
```

## 隱私

這個工具只讀取本機 Codex Desktop 檔案，不會上傳任何內容。

分享前請自己再看一次匯出的 Markdown。工具會過濾內部紀錄，但你自己輸入的對話仍然可能包含私人資訊。

## 歡迎貢獻

歡迎大家一起加功能。你可以新增輸出格式、改善過濾規則、做簡單 UI、支援更多平台，或讓流程更順手。

保持小巧、實用，也讓想取回自己對話的人少一點麻煩。

## 授權

Apache License 2.0。
