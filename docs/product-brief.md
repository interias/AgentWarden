# Product Brief

Agent Warden is a minimal local overlay for monitoring background AI coding agents while the user is focused elsewhere, especially while gaming in borderless-windowed mode.

The first supported target is OpenAI Codex. The MVP watches local Codex session files and infers basic state from filesystem metadata.

## Product Goals

- Show whether watched agents appear active, idle, finished, failed, or in need of attention.
- Keep the app extremely lightweight and robust.
- Run fully locally on Windows.
- Avoid cloud services, telemetry, accounts, and hidden background complexity.
- Start with Codex while keeping the watcher architecture agent-neutral.
- Protect private prompts and completions by default.

## Target User

The first user is a developer who starts long-running AI coding agents and then switches context, for example into a game running in borderless-windowed mode. The overlay should answer one practical question quickly: "Do I need to look back at my agents?"

## MVP Scope

Included:

- Windows-first Python application.
- Tkinter always-on-top overlay.
- Codex watcher scanning `%USERPROFILE%\.codex\sessions\**\*.jsonl`.
- Polling every 10 seconds by default.
- Configurable polling interval from 5 to 60 seconds.
- Metadata-only session status: agent, session id, path, last modified time, inferred state, optional safe workspace name.
- One-shot CLI scan for debugging.
- VS Code tasks for starting, scanning, and testing.
- Fixed overlay positions: top-left, top-right, bottom-left, bottom-right.
- Installable VS Code extension for controlling the local overlay.

Not included:

- Cloud backend.
- Telemetry.
- Account system.
- Real-time filesystem event watching.
- Packaged Windows `.exe`.
- Parsing or displaying private prompt/completion contents.
- Multi-agent support beyond the initial Codex watcher.
- Reimplementing watcher logic in TypeScript.

## Current Status Semantics

The MVP status model includes:

- `active`: session file was modified recently.
- `idle`: session file exists but was not modified recently.
- `finished`: session file has not changed for several hours.
- `failed`: reserved for future explicit event parsing.
- `needs_attention`: reserved for future explicit event parsing.
- `unknown`: no sessions found or state cannot be inferred.

`failed` and `needs_attention` are part of the model but should stay conservative until a privacy-reviewed event parser exists.

## Success Criteria

The MVP is useful when:

- It can be started from PowerShell and VS Code.
- It detects local Codex activity without reading session contents.
- It uses little CPU and memory while polling.
- The overlay stays small, readable, and unobtrusive.
- The default overlay position is top-right, with CLI/config options for other fixed corners.
- The user can run `--once` to verify what Agent Warden sees.
- The project remains simple enough to modify without a framework-heavy setup.
