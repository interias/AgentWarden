# Decisions

## 2026-05-09: Stdlib-first MVP

Agent Warden starts with a stdlib-first Python implementation. Tkinter is the first overlay toolkit, and the watcher uses polling instead of `watchdog`.

## 2026-05-09: Metadata-only Codex watcher

The first Codex watcher infers state from JSONL file modification times only. It does not read or parse session event payloads.

## 2026-05-09: English project docs

Project docs and agent instructions are written in English for open-source contributor accessibility.

## 2026-05-09: MIT license

Agent Warden uses the MIT License so people can freely use, modify, distribute, and build on the project with minimal restrictions.

## 2026-05-09: Documentation source split

Documentation is split by audience and source of truth:

- root `README.md` for public quickstart
- `docs/product-brief.md` for product scope
- `docs/architecture.md` for technical shape
- `docs/development.md` for local workflow
- `docs/privacy.md` for data handling rules
- `docs/ai/` for compact agent memory

## 2026-05-09: Overlay default position

The overlay defaults to the top-right corner because it is less likely to cover common game HUD elements and developer terminal prompts than the top-left corner. Users can select any fixed corner through config or CLI.
