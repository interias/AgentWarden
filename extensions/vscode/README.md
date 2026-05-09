# Agent Warden VS Code Extension

Agent Warden for VS Code controls the local Agent Warden Python overlay without duplicating watcher logic in TypeScript.

## Commands

- `Agent Warden: Start`
- `Agent Warden: Stop`
- `Agent Warden: Restart`
- `Agent Warden: Scan Once`
- `Agent Warden: Set Position`
- `Agent Warden: Show Output`
- `Agent Warden: Commands`

Clicking the Agent Warden status bar item opens the command menu directly.

## Settings

- `agentWarden.position`
- `agentWarden.pollIntervalSeconds`
- `agentWarden.activeThresholdSeconds`
- `agentWarden.opacity`
- `agentWarden.sessionsRoot`
- `agentWarden.pythonPath`
- `agentWarden.autoStart`

The extension is local-only. It does not add telemetry, cloud services, or JSONL content parsing.
