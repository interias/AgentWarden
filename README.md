# Agent Warden

Agent Warden is a tiny, local-first Windows overlay for monitoring background AI coding agents. The MVP watches local OpenAI Codex session files and shows a compact always-on-top status indicator while you are gaming or working in another window.

The project is intentionally minimal:

- Python-first and Windows-first.
- Local only.
- No cloud backend.
- No telemetry.
- No private prompt or completion display.
- Polling-based status updates every 10 seconds by default.
- Stdlib Tkinter overlay for the MVP.

## Current MVP

Agent Warden currently:

- Scans Codex session files under `%USERPROFILE%\.codex\sessions`.
- Uses file metadata only: path, session id, modification time, inferred state.
- Infers `active`, `idle`, and `finished` states from modification age.
- Shows a small Tkinter overlay in the top-right corner by default.
- Provides a one-shot CLI scan for debugging and validation.
- Includes VS Code tasks and a VS Code extension for starting, stopping, scanning, and configuring the overlay.

It does not parse JSONL event contents.

## Quickstart

From a PowerShell terminal:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m agent_warden
```

Or use the helper script, which creates `.venv` and installs requirements if needed:

```powershell
.\scripts\start-agent-warden.ps1
```

Run a metadata-only scan without opening the overlay:

```powershell
python -m agent_warden --once
.\scripts\start-agent-warden.ps1 -Once
```

In VS Code, use `Terminal > Run Task...`:

- `Agent Warden: Start Overlay`
- `Agent Warden: Scan Once`
- `Agent Warden: Test`

The installable VS Code extension lives in `extensions/vscode/`. It controls the Python overlay without duplicating watcher logic.

## Configuration

Agent Warden runs without a config file. If present, it reads JSON from:

```text
%APPDATA%\AgentWarden\config.json
```

Example:

```json
{
  "poll_interval_seconds": 10,
  "codex_sessions_root": "C:\\Users\\you\\.codex\\sessions",
  "active_threshold_seconds": 60,
  "overlay_x": 24,
  "overlay_y": 24,
  "overlay_opacity": 0.92,
  "overlay_position": "top-right"
}
```

Useful runtime overrides:

```powershell
python -m agent_warden --once --sessions-root "$env:USERPROFILE\.codex\sessions"
python -m agent_warden --poll-interval 10 --active-threshold 60 --opacity 0.92 --position top-right
```

`poll_interval_seconds` must be between 5 and 60 seconds.
`overlay_position` can be `top-left`, `top-right`, `bottom-left`, or `bottom-right`.
`overlay_x` and `overlay_y` are margins from the selected corner.

## Documentation

Start with [docs/README.md](docs/README.md).

Key documents:

- [Product brief](docs/product-brief.md)
- [Architecture](docs/architecture.md)
- [Development guide](docs/development.md)
- [Privacy model](docs/privacy.md)
- [Codex agent instructions](AGENTS.md)

## Development

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pytest
python -m compileall -q src
git diff --check
```

Dependencies are declared in `pyproject.toml`. `requirements.txt` is a convenience entrypoint for local development.

Build the VS Code extension:

```powershell
cd extensions\vscode
npm install
npm run compile
npm test
npm run package
code --install-extension .\agent-warden-0.1.0.vsix
```

If `code --install-extension` resolves to `Code.exe` directly on Windows, use `%LOCALAPPDATA%\Programs\Microsoft VS Code\bin\code.cmd` instead.

## License

Agent Warden is released under the MIT License. You can use, modify, distribute, and build on it freely under the terms in [LICENSE](LICENSE).
