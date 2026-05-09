# Development Guide

This guide covers local setup, common commands, VS Code tasks, and verification for Agent Warden.

## Requirements

- Windows.
- Python 3.12 or newer.
- Python 3.13 is the current local development baseline.
- PowerShell for helper scripts and VS Code tasks.
- Node.js and npm for the VS Code extension.

The project has no runtime dependencies outside the Python standard library. Development dependencies are declared in `pyproject.toml` and installed through `requirements.txt`.

## First Setup

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

If `py -3.13` is unavailable, use a Python 3.12+ interpreter:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Running Agent Warden

Start the overlay:

```powershell
python -m agent_warden
```

Run a one-shot metadata scan:

```powershell
python -m agent_warden --once
```

Use runtime overrides:

```powershell
python -m agent_warden --once --sessions-root "$env:USERPROFILE\.codex\sessions"
python -m agent_warden --poll-interval 10 --active-threshold 60 --opacity 0.92 --position top-right
```

## Helper Script

The helper script creates `.venv` if needed and installs `requirements.txt` if the package is not importable.

```powershell
.\scripts\start-agent-warden.ps1
.\scripts\start-agent-warden.ps1 -Once
```

Parameters:

- `-Once`: run a one-shot metadata scan instead of opening the overlay.
- `-SessionsRoot <path>`: override the Codex sessions folder.
- `-PollInterval <seconds>`: override polling interval.
- `-ActiveThreshold <seconds>`: override active status threshold.
- `-Opacity <value>`: override overlay opacity.
- `-Position <corner>`: choose `top-left`, `top-right`, `bottom-left`, or `bottom-right`.

## VS Code Tasks

Run `Terminal > Run Task...` and choose:

- `Agent Warden: Start Overlay`
- `Agent Warden: Scan Once`
- `Agent Warden: Test`

The tasks call the same PowerShell helper script used from the terminal.

## VS Code Extension

The installable extension lives in `extensions/vscode/`.

```powershell
cd extensions\vscode
npm install
npm run compile
npm test
npm run package
code --install-extension .\agent-warden-0.1.0.vsix
```

If `code --install-extension` resolves to `Code.exe` directly and reports `bad option`, run the CLI script explicitly:

```powershell
& "$env:LOCALAPPDATA\Programs\Microsoft VS Code\bin\code.cmd" --install-extension .\agent-warden-0.1.0.vsix --force
```

The extension bundles the Python package during packaging:

```powershell
npm run prepare-python
```

Extension commands:

- `Agent Warden: Start`
- `Agent Warden: Stop`
- `Agent Warden: Restart`
- `Agent Warden: Scan Once`
- `Agent Warden: Set Position`
- `Agent Warden: Show Output`
- `Agent Warden: Commands`

The status bar item uses the Agent Warden icon and opens the command menu on click.

## Verification

Use the project virtual environment:

```powershell
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe -m compileall -q src
git diff --check
```

For a local smoke test:

```powershell
.\scripts\start-agent-warden.ps1 -Once
```

For extension checks:

```powershell
cd extensions\vscode
npm run compile
npm test
npm run package
```

Do not claim a check passed unless it was run.

## Dependency Policy

- Keep runtime dependencies at zero unless a dependency is clearly necessary.
- Declare dependencies in `pyproject.toml`.
- Keep `requirements.txt` as a convenience file pointing to `-e .[dev]`.
- Keep VS Code extension dependencies scoped under `extensions/vscode/package.json`.
- Do not add watcher, GUI, or packaging dependencies without updating `docs/architecture.md` and `docs/ai/DECISIONS.md`.

## Workspace Hygiene

Ignored local files include:

- `.venv/`
- `__pycache__/`
- `.pytest_cache/`
- build artifacts
- local `.env` files
- local logs
- extension `node_modules/`, `out/`, bundled `python/`, and `*.vsix`

`.vscode/tasks.json` is intentionally tracked. Other `.vscode` files remain ignored.
