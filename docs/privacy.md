# Privacy Model

Agent Warden is local-first and privacy-preserving by default.

## Core Rules

- No cloud backend.
- No telemetry.
- No account system.
- No network calls for monitoring.
- No VS Code extension telemetry.
- No prompt or completion display.
- No JSONL event payload parsing in the MVP.
- No sensitive raw data in logs, docs, tests, or memory files.

## Data Read By The MVP

The Codex watcher reads filesystem metadata from local session files:

- file path
- file name or stem for session id
- file modification time
- existence of matching `*.jsonl` files

The watcher does not open JSONL files to inspect event contents.

The VS Code extension starts the Python Core and reads command output. It does not scan Codex files itself and does not add a second telemetry or parsing path.

## Data Shown To The User

The overlay and one-shot CLI scan may show:

- agent name
- session id derived from file name
- inferred status
- last modified timestamp
- optional safe workspace name if inferred without reading private content

They must not show:

- prompt text
- completion text
- hidden reasoning
- file event payloads
- tokens or credentials
- arbitrary JSONL fields

## Future Event Parsing

Future support for `failed`, `finished`, or `needs_attention` from Codex event contents requires a separate design decision.

Minimum requirements before adding event parsing:

- explicit allowlist of event types
- explicit allowlist of fields
- tests proving private prompt/completion content is not returned
- documentation update in `docs/architecture.md`
- decision entry in `docs/ai/DECISIONS.md`

## Logging

The MVP should avoid persistent logs. If logs are later added, they must contain operational metadata only and must never include prompts, completions, tokens, image data, or raw session events.
