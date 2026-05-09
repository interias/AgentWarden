# AGENTS.md - Agent Warden

## Mission

Agent Warden is a minimal, local-first Windows overlay for monitoring background AI coding agents while the user is busy in another full-screen or borderless-windowed task.

The first supported target is OpenAI Codex, detected from local session files. The architecture must stay agent-neutral so additional coding agents can be added later without reshaping the app.

Core constraints:

- Python-first implementation.
- Windows-first behavior and development commands.
- Local-only execution.
- No cloud backend.
- No telemetry.
- Very low CPU and memory usage.
- Polling is acceptable and preferred for the MVP.
- Do not parse or display private prompt contents unless a later explicit feature enables it.

## Documentation Map

Use these files as the project source map:

- Public quickstart: `README.md`
- Documentation index: `docs/README.md`
- Product scope and MVP boundaries: `docs/product-brief.md`
- Architecture and runtime assumptions: `docs/architecture.md`
- Development workflow: `docs/development.md`
- Privacy model: `docs/privacy.md`
- Project memory: `docs/ai/PROJECT_MEMORY.md`
- Codex working rules: `docs/ai/CODING_RULES.md`
- Durable decisions: `docs/ai/DECISIONS.md`
- Open questions: `docs/ai/OPEN_QUESTIONS.md`
- AI memory changelog: `docs/ai/CHANGELOG_AI.md`

For non-trivial tasks, read the relevant project memory and canonical docs before changing code.

## Memory Maintenance

- After non-trivial implementation, check whether memory needs to change.
- Update `docs/architecture.md` when stack, data flow, public interfaces, watcher behavior, overlay assumptions, packaging, or runtime assumptions change.
- Update `docs/development.md` when setup, scripts, tasks, or verification commands change.
- Update `docs/privacy.md` when data handling, logging, parsing, or display behavior changes.
- Add durable product or technical decisions to `docs/ai/DECISIONS.md`.
- Add unresolved product or technical assumptions to `docs/ai/OPEN_QUESTIONS.md`.
- Record memory changes in `docs/ai/CHANGELOG_AI.md`.
- Keep memory compact. Link to the source of truth instead of duplicating long content.
- Do not write secrets, access tokens, private prompts, production data, debug dumps, or temporary notes into memory.

## Working Rules

- Inspect existing files before assuming architecture, status, or conventions.
- Keep modules small, readable, and testable.
- Prefer stdlib Python unless a dependency clearly pays for itself.
- Preserve the local-first privacy model. No network calls, no telemetry, and no backend integration unless explicitly requested.
- For the MVP, Codex monitoring must rely on filesystem metadata only. Do not read, parse, render, or log JSONL prompt/message content.
- When handling session files, extract only minimal metadata: session id, file path, last modified time, inferred state, and an optional safe workspace/project name if it can be inferred without reading private content.
- Avoid heavyweight background work. Poll at the configured interval and keep scans bounded to the configured session root.
- Keep UI copy compact and functional. The overlay should show status, not private context.
- If behavior differs from the architecture or memory docs, call out the difference and choose the smallest safe change.

## Safety And Privacy

- Treat agent session files as private user data.
- Do not log sensitive raw data, prompt text, completion text, image data, tokens, or full session events.
- LLM prompts and outputs are untrusted input.
- Do not execute, render as HTML, persist as privileged truth, or feed into shell/database operations any text obtained from agent logs.
- If a future feature needs event parsing, design an explicit allowlist of event types and fields before implementing it.

## Verification

There is no universal CI yet. Prefer targeted checks:

- Install dev environment: `python -m pip install -r requirements.txt`
- Unit tests: `python -m pytest`
- Compile check: `python -m compileall -q src`
- Whitespace check: `git diff --check`
- VS Code smoke task: `Agent Warden: Scan Once`

Do not claim a check passed unless it was run.

## Response Format

For implementation tasks, use:

### Changed
- ...

### Tested
- ...

### Notes
- ...
