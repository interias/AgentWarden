# Coding Rules

These rules guide implementation work in Agent Warden.

## General

- Keep implementation small and explicit.
- Prefer stdlib Python before adding dependencies.
- Keep modules testable without launching the overlay.
- Use dataclasses and enums for simple structured data.
- Use `pathlib.Path` for filesystem paths.
- Make Windows behavior the default, but keep tests portable where practical.

## Privacy And Data Handling

- Do not parse or expose private Codex prompt/completion content in the MVP.
- Do not add network calls or telemetry.
- Do not log raw session event payloads.
- When changing data handling, update `docs/privacy.md`.

## Dependencies

- Keep Python dependency declarations centralized in `pyproject.toml`.
- Keep `requirements.txt` as a convenience install entrypoint.
- Do not add runtime dependencies without updating `docs/architecture.md` and `docs/ai/DECISIONS.md`.

## Verification

Before finalizing implementation work, run targeted checks and state exactly what passed.

Default checks:

```powershell
python -m pytest
python -m compileall -q src
git diff --check
```

When touching scripts or VS Code tasks, also run:

```powershell
.\scripts\start-agent-warden.ps1 -Once
```
