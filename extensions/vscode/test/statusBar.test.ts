import * as assert from "assert";
import test from "node:test";

import {
  AGENT_WARDEN_MENU_COMMAND,
  AGENT_WARDEN_STATUS_ICON,
  AGENT_WARDEN_STATUS_TOOLTIP,
  formatStatusBarText,
} from "../src/statusBar";

test("formatStatusBarText uses the Agent Warden status icon", () => {
  assert.equal(AGENT_WARDEN_STATUS_ICON, "$(hubot)");
  assert.equal(formatStatusBarText("running"), "$(hubot) Agent Warden: running");
});

test("status bar opens the Agent Warden command menu", () => {
  assert.equal(AGENT_WARDEN_MENU_COMMAND, "agentWarden.openMenu");
  assert.equal(AGENT_WARDEN_STATUS_TOOLTIP, "Agent Warden commands");
});
