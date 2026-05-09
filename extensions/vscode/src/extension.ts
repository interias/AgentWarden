import * as vscode from "vscode";

import { AgentWardenController, AgentWardenStatus } from "./controller";
import { POSITIONS, resolveAgentWardenConfig } from "./config";
import {
  AGENT_WARDEN_MENU_COMMAND,
  AGENT_WARDEN_STATUS_TOOLTIP,
  formatStatusBarText,
} from "./statusBar";

type AgentWardenMenuItem = vscode.QuickPickItem & {
  command: string;
};

const COMMAND_MENU_ITEMS: readonly AgentWardenMenuItem[] = [
  {
    label: "$(debug-start) Start",
    description: "Start overlay",
    command: "agentWarden.start",
  },
  {
    label: "$(debug-stop) Stop",
    description: "Stop overlay",
    command: "agentWarden.stop",
  },
  {
    label: "$(debug-restart) Restart",
    description: "Restart overlay",
    command: "agentWarden.restart",
  },
  {
    label: "$(search) Scan Once",
    description: "Run a metadata-only scan",
    command: "agentWarden.scanOnce",
  },
  {
    label: "$(location) Set Position",
    description: "Choose overlay corner",
    command: "agentWarden.setPosition",
  },
  {
    label: "$(output) Show Output",
    description: "Open the Agent Warden output",
    command: "agentWarden.showOutput",
  },
];

let controller: AgentWardenController | undefined;
let statusBar: vscode.StatusBarItem | undefined;

export function activate(context: vscode.ExtensionContext): void {
  const output = vscode.window.createOutputChannel("Agent Warden");
  statusBar = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 100);
  controller = new AgentWardenController(output, updateStatusBar);

  updateStatusBar("stopped");
  statusBar.show();

  context.subscriptions.push(output, statusBar);
  context.subscriptions.push(
    vscode.commands.registerCommand("agentWarden.start", async () => {
      await runSafely(output, async () => {
        controller?.start(readConfig(context));
      });
    }),
    vscode.commands.registerCommand("agentWarden.stop", async () => {
      await runSafely(output, async () => {
        await controller?.stop();
      });
    }),
    vscode.commands.registerCommand("agentWarden.restart", async () => {
      await runSafely(output, async () => {
        await controller?.restart(readConfig(context));
      });
    }),
    vscode.commands.registerCommand("agentWarden.scanOnce", async () => {
      await runSafely(output, async () => {
        output.show(true);
        const result = await controller?.scanOnce(readConfig(context));
        if (result) {
          output.appendLine("");
          output.appendLine(result);
        }
      });
    }),
    vscode.commands.registerCommand("agentWarden.setPosition", async () => {
      await runSafely(output, async () => {
        const selected = await vscode.window.showQuickPick([...POSITIONS], {
          title: "Agent Warden Position",
          placeHolder: "Select overlay position",
        });
        if (!selected) {
          return;
        }

        await vscode.workspace
          .getConfiguration("agentWarden")
          .update("position", selected, vscode.ConfigurationTarget.Global);

        if (controller?.isRunning()) {
          await controller.restart(readConfig(context));
        }
      });
    }),
    vscode.commands.registerCommand("agentWarden.showOutput", () => {
      output.show(true);
    }),
    vscode.commands.registerCommand(AGENT_WARDEN_MENU_COMMAND, async () => {
      await runSafely(output, async () => {
        const selected = await vscode.window.showQuickPick(COMMAND_MENU_ITEMS, {
          title: "Agent Warden",
          placeHolder: "Choose a command",
        });
        if (!selected) {
          return;
        }

        await vscode.commands.executeCommand(selected.command);
      });
    }),
  );

  const config = readConfig(context);
  if (config.autoStart) {
    controller.start(config);
  }
}

export async function deactivate(): Promise<void> {
  await controller?.stop();
}

function readConfig(context: vscode.ExtensionContext) {
  const configuration = vscode.workspace.getConfiguration("agentWarden");
  return resolveAgentWardenConfig(
    {
      get: <T>(key: string, defaultValue: T): T => configuration.get<T>(key, defaultValue),
    },
    context.extensionPath,
  );
}

async function runSafely(output: vscode.OutputChannel, action: () => Promise<void>): Promise<void> {
  try {
    await action();
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    output.appendLine(`Agent Warden error: ${message}`);
    output.show(true);
    updateStatusBar("error");
    void vscode.window.showErrorMessage(message);
  }
}

function updateStatusBar(status: AgentWardenStatus): void {
  if (!statusBar) {
    return;
  }

  statusBar.text = formatStatusBarText(status);
  statusBar.command = AGENT_WARDEN_MENU_COMMAND;
  statusBar.tooltip = AGENT_WARDEN_STATUS_TOOLTIP;
}
