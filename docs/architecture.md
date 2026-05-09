# Architecture

Agent Warden is a small Python application with three main parts:

- Configuration loading.
- Agent watchers that return metadata-only session status.
- A Tkinter overlay that polls watchers and renders aggregate state.
- A VS Code extension that controls the Python app without reimplementing watcher logic.

The architecture is intentionally conservative. The MVP favors predictable polling and stdlib UI over real-time filesystem subscriptions, background services, or a larger GUI framework.

## Runtime Model

The app runs locally as a normal Python process. It does not open network connections and does not send telemetry.

Default behavior:

- Poll every 10 seconds.
- Allow polling interval values from 5 to 60 seconds.
- Watch Codex session files under `%USERPROFILE%\.codex\sessions`.
- Render a small always-on-top overlay.
- Place the overlay in the top-right corner by default.
- Use runtime CLI flags to override config values without writing persistent settings.

## Package Layout

Primary package: `src/agent_warden/`

- `app.py`: CLI parsing, config loading, watcher construction, one-shot scan, overlay launch.
- `config.py`: `AppConfig`, config defaults, JSON loading, runtime overrides.
- `models.py`: shared status enums and dataclasses.
- `watchers/base.py`: watcher protocol.
- `watchers/codex.py`: Codex filesystem watcher.
- `overlay/tkinter_overlay.py`: Tkinter window implementation.
- `overlay/summary.py`: pure overlay summary formatting.

Tests live in `tests/` and avoid launching the visible overlay.

VS Code extension package: `extensions/vscode/`

- `src/extension.ts`: command registration, statusbar, output channel.
- `src/controller.ts`: extension-owned process control.
- `src/config.ts`: settings resolution and Python launch argument construction.
- `scripts/prepare-python.js`: copies `src/agent_warden` into the VSIX package.
- `test/`: Node tests for pure extension helper logic.

## Data Model

`AgentState` values:

- `active`
- `idle`
- `finished`
- `failed`
- `needs_attention`
- `unknown`

`AgentSessionStatus` contains only metadata:

- agent name
- session id
- local path
- last modified timestamp
- inferred state
- optional safe workspace name
- optional non-private reason

`WatcherSnapshot` contains:

- tuple of `AgentSessionStatus`
- scan timestamp
- aggregate state derived from session state priority
- counts by state

## Configuration

Agent Warden runs without a config file. If present, it reads:

```text
%APPDATA%\AgentWarden\config.json
```

Supported fields:

- `poll_interval_seconds`: integer, 5 to 60, default `10`.
- `codex_sessions_root`: path, default `%USERPROFILE%\.codex\sessions`.
- `active_threshold_seconds`: positive integer, default `60`.
- `overlay_x`: integer, default `24`.
- `overlay_y`: integer, default `24`.
- `overlay_opacity`: float, 0.2 to 1.0, default `0.92`.
- `overlay_position`: one of `top-left`, `top-right`, `bottom-left`, `bottom-right`, default `top-right`.

`overlay_x` and `overlay_y` are margins from the selected fixed corner.

Runtime CLI flags can override these values for the current process.

## Codex Watcher

The Codex watcher scans:

```text
%USERPROFILE%\.codex\sessions\**\*.jsonl
```

The MVP uses only:

- `Path.rglob("*.jsonl")`
- `Path.stat()`
- file stem for session id
- file modification timestamp for state inference

Status inference:

- recently modified files are `active`
- files older than the active threshold but newer than the finished threshold are `idle`
- files not modified for several hours are `finished`

The watcher must not read prompt text, completion text, or JSONL event payloads in the MVP.

## Overlay

The first overlay implementation uses stdlib Tkinter:

- frameless window
- always-on-top attribute
- configurable opacity
- compact aggregate Codex status
- current-session-focused summary so old finished history does not dominate the overlay
- fixed corner positioning, defaulting to top-right
- periodic refresh via Tkinter `after()`

The overlay refresh re-applies the topmost attribute. If this is not reliable enough for common borderless-windowed games, a future decision can add targeted Windows APIs such as `pywin32`.

## Resource Strategy

The MVP keeps resource usage low by:

- polling at a bounded interval
- avoiding file content reads
- using simple dataclasses and enums
- keeping UI rendering to two labels
- sorting only metadata for discovered JSONL files
- avoiding background threads until there is a measured need

If Codex histories become very large, the next optimization should limit scanning to recent date folders or cache unchanged file metadata.

## Public Interfaces

CLI:

```powershell
python -m agent_warden
python -m agent_warden --once
python -m agent_warden --sessions-root "<path>"
python -m agent_warden --poll-interval 10 --active-threshold 60 --opacity 0.92 --position top-right
```

Helper script:

```powershell
.\scripts\start-agent-warden.ps1
.\scripts\start-agent-warden.ps1 -Once
```

VS Code tasks:

- `Agent Warden: Start Overlay`
- `Agent Warden: Scan Once`
- `Agent Warden: Test`

VS Code extension commands:

- `Agent Warden: Start`
- `Agent Warden: Stop`
- `Agent Warden: Restart`
- `Agent Warden: Scan Once`
- `Agent Warden: Set Position`
- `Agent Warden: Show Output`
- `Agent Warden: Commands`

The extension status bar item opens this command menu directly.

The extension bundles the Python package into the VSIX and starts it with `PYTHONPATH=<extension>/python`. In development mode it falls back to the repository `src` directory.

## Extension Points

Future watchers should implement the `AgentWatcher` protocol and return `WatcherSnapshot`.

Future event parsing must be designed explicitly before implementation. It should use an allowlist of non-private event types and fields, and it must not expose prompt or completion content.

The VS Code extension must remain a control layer. It should not duplicate Codex watcher behavior in TypeScript unless a later decision changes the architecture.
