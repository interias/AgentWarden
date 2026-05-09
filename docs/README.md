# Agent Warden Documentation

This directory contains the project documentation and AI working memory for Agent Warden.

## Start Here

- `README.md` at the repository root is the public quickstart.
- `AGENTS.md` at the repository root is the Codex entrypoint for agentic work.
- `docs/product-brief.md` defines what Agent Warden is building.
- `docs/architecture.md` defines the current technical shape.
- `docs/development.md` explains local setup, scripts, VS Code tasks, and checks.
- `docs/privacy.md` defines the privacy and data handling rules.

## AI Memory

The `docs/ai/` files are compact working memory for Codex and other coding agents:

- `PROJECT_MEMORY.md` tracks current project state and source map.
- `CODING_RULES.md` records durable implementation rules.
- `DECISIONS.md` records durable product and technical decisions.
- `OPEN_QUESTIONS.md` tracks unresolved questions.
- `CHANGELOG_AI.md` records changes to AI-facing memory.

Do not duplicate long content in AI memory. Link to the canonical document instead.

## Source Of Truth

- Product scope and MVP boundaries: `docs/product-brief.md`
- Runtime architecture and interfaces: `docs/architecture.md`
- Local development workflow: `docs/development.md`
- Privacy constraints: `docs/privacy.md`
- Agent behavior and maintenance rules: `AGENTS.md`

When a change affects more than one document, update the canonical source first and then adjust references.
