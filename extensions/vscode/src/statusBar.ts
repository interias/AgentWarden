import type { AgentWardenStatus } from "./controller";

export const AGENT_WARDEN_MENU_COMMAND = "agentWarden.openMenu";
export const AGENT_WARDEN_STATUS_ICON = "$(hubot)";
export const AGENT_WARDEN_STATUS_TOOLTIP = "Agent Warden commands";

export function formatStatusBarText(status: AgentWardenStatus): string {
  return `${AGENT_WARDEN_STATUS_ICON} Agent Warden: ${status}`;
}
