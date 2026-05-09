# Project Memory

Agent Warden is an open-source, Windows-first, local-only Python overlay for monitoring background AI coding agents.

## Current State

- Initial architecture scaffold is established.
- Project license is MIT.
- Runtime package is `agent_warden`.
- Current watcher target is OpenAI Codex local session files.
- Current overlay implementation is Tkinter.
- Local development uses `.venv`, `requirements.txt`, a PowerShell start script, and VS Code tasks.
- Current status inference is metadata-only and based on file modification time.
- A VS Code extension under `extensions/vscode/` controls the Python app as a launcher/status/settings layer.

## Canonical Sources

- Project quickstart: `README.md`
- Documentation map: `docs/README.md`
- Product scope: `docs/product-brief.md`
- Architecture: `docs/architecture.md`
- Development workflow: `docs/development.md`
- Privacy model: `docs/privacy.md`
- Agent instructions: `AGENTS.md`

## Current Implementation Map

- CLI and app orchestration: `src/agent_warden/app.py`
- Config loading and runtime overrides: `src/agent_warden/config.py`
- Status dataclasses and enums: `src/agent_warden/models.py`
- Codex metadata watcher: `src/agent_warden/watchers/codex.py`
- Tkinter overlay: `src/agent_warden/overlay/tkinter_overlay.py`
- Overlay summary formatting: `src/agent_warden/overlay/summary.py`
- Start script: `scripts/start-agent-warden.ps1`
- VS Code tasks: `.vscode/tasks.json`
- VS Code extension: `extensions/vscode/`

Keep this file compact. Put durable technical detail in the canonical docs instead.
