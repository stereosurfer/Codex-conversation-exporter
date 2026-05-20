# Codex 對話匯出器

# Codex Conversation Exporter

把 Mac 上的 Codex Desktop 本機對話匯出成乾淨的 Markdown。

Export local Codex Desktop conversations on macOS to clean Markdown.

這是一個小而實用的工具。它適合想保存、搜尋或分享某幾段 Codex 對話的人，不用再手動一段一段複製。

This is a small, friendly tool for people who want to keep, search, or share selected Codex conversations without copying the whole chat by hand.

**目前只支援 Mac。** 它讀取 Codex Desktop 在 `~/.codex/` 底下的本機檔案，所以目前定位是 macOS 工具。

**Mac only for now.** It reads Codex Desktop's local files under `~/.codex/`, which currently makes this a macOS-focused tool.

## 功能

## Features

- 列出最近的 Codex 對話
- List recent Codex conversations
- 匯出最新對話
- Export the latest conversation
- 用標題關鍵字匯出
- Export by title keyword
- 用 thread id 匯出
- Export by thread id
- 輸出乾淨 Markdown
- Save clean Markdown
- 過濾 system/developer prompt、工具呼叫、加密推理與 raw logs
- Filter out system/developer prompts, tool calls, encrypted reasoning, and raw logs

## 安裝

## Install

先打開 Mac 的「終端機」。

First, open Terminal on your Mac.

把下面三行貼進去，按 Enter。

Paste these three lines, then press Enter.

```bash
git clone https://github.com/stereosurfer/Codex-conversation-exporter.git
cd Codex-conversation-exporter
python3 -m pip install -e .
```

## 如何使用

## How to Use

### 1. 先看看有哪些對話

### 1. See your conversations

在終端機貼上這行：

Paste this in Terminal:

```bash
codex-conversation-exporter --list
```

你會看到一串對話清單。每一行會有時間、id、標題。

You will see a list of conversations. Each line has a time, an id, and a title.

### 2. 匯出最新的一個對話

### 2. Export the latest conversation

如果你只想匯出最新對話，貼上這行：

If you only want the latest conversation, paste this:

```bash
codex-conversation-exporter --latest
```

它會產生一個 Markdown 檔案。

It will create a Markdown file.

### 3. 用標題找對話

### 3. Find a conversation by title

如果你記得標題裡有某個字，例如「project planning」，貼上：

If you remember a word in the title, like "project planning", paste:

```bash
codex-conversation-exporter --query "project planning"
```

中文也可以，例如：

Chinese works too, for example:

```bash
codex-conversation-exporter --query "專案規劃"
```

### 4. 用 thread id 匯出

### 4. Export by thread id

如果你知道完整 thread id，貼上：

If you know the full thread id, paste:

```bash
codex-conversation-exporter --id 01234567-89ab-cdef-0123-456789abcdef
```

### 5. 找到匯出的檔案

### 5. Find the exported file

預設匯出到：

By default, exports are saved to:

```text
~/Documents/AI Conversation Records/
```

檔名長這樣：

File names look like this:

```text
YYYY-MM-DD_HHMMSS__thread-title__thread-shortid.md
```

你可以用任何 Markdown 編輯器打開它，也可以直接用一般文字編輯器看。

You can open it with any Markdown editor, or just read it with a normal text editor.

## 隱私

## Privacy

這個工具只讀取你 Mac 上的 Codex Desktop 本機檔案，不會上傳任何內容。

This tool only reads local Codex Desktop files on your Mac. It does not upload anything.

分享前請自己再看一次匯出的 Markdown。工具會過濾內部紀錄，但你自己輸入的對話仍然可能包含私人資訊。

Please review exported Markdown before sharing it. The exporter filters internal records, but your conversations may still contain private information that you typed.

## 歡迎貢獻

## Contributing

歡迎大家一起加功能。你可以新增輸出格式、改善過濾規則、做簡單 UI、支援更多平台，或讓流程更順手。

Contributions are welcome. Add a new output format, improve filtering, build a simple UI, support more platforms, or make the workflow smoother.

保持小巧、實用，也讓想取回自己對話的人少一點麻煩。

Keep it small, useful, and kind to people who just want their conversations back.

## 授權

## License

Apache License 2.0。

Apache License 2.0.
