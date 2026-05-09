import { ChildProcessWithoutNullStreams, spawn } from "child_process";

import { AgentWardenConfig, buildLaunchSpec } from "./config";

export type AgentWardenStatus = "stopped" | "running" | "error";

export interface OutputSink {
  append(value: string): void;
  appendLine(value: string): void;
  show(preserveFocus?: boolean): void;
}

export function statusFromProcessClose(
  intentionalStop: boolean,
  code: number | null,
): AgentWardenStatus {
  if (intentionalStop || code === 0) {
    return "stopped";
  }
  return "error";
}

export class AgentWardenController {
  private child: ChildProcessWithoutNullStreams | undefined;
  private intentionalStop = false;

  constructor(
    private readonly output: OutputSink,
    private readonly onStatusChanged: (status: AgentWardenStatus) => void,
  ) {}

  isRunning(): boolean {
    return this.child !== undefined;
  }

  start(config: AgentWardenConfig): boolean {
    if (this.child) {
      this.output.appendLine("Agent Warden is already running.");
      return false;
    }

    const launch = buildLaunchSpec(config, false);
    this.intentionalStop = false;
    this.output.appendLine(`Starting Agent Warden: ${launch.command} ${launch.args.join(" ")}`);

    const child = spawn(launch.command, launch.args, {
      cwd: config.extensionPath,
      env: launch.env,
      windowsHide: true,
    });

    this.child = child;
    this.onStatusChanged("running");

    child.stdout.on("data", (chunk: Buffer) => this.output.append(chunk.toString()));
    child.stderr.on("data", (chunk: Buffer) => this.output.append(chunk.toString()));
    child.on("error", (error) => {
      this.output.appendLine(`Agent Warden failed to start: ${error.message}`);
      this.child = undefined;
      this.onStatusChanged("error");
    });
    child.on("close", (code) => {
      const status = statusFromProcessClose(this.intentionalStop, code);
      this.output.appendLine(`Agent Warden process exited with code ${code ?? "unknown"}.`);
      this.child = undefined;
      this.intentionalStop = false;
      this.onStatusChanged(status);
    });

    return true;
  }

  async stop(): Promise<boolean> {
    if (!this.child) {
      this.output.appendLine("Agent Warden is not running.");
      this.onStatusChanged("stopped");
      return false;
    }

    const child = this.child;
    this.intentionalStop = true;
    child.kill();
    await new Promise<void>((resolve) => child.once("close", () => resolve()));
    return true;
  }

  async restart(config: AgentWardenConfig): Promise<void> {
    if (this.child) {
      await this.stop();
    }
    this.start(config);
  }

  async scanOnce(config: AgentWardenConfig): Promise<string> {
    const launch = buildLaunchSpec(config, true);
    this.output.appendLine(`Scanning once: ${launch.command} ${launch.args.join(" ")}`);

    return new Promise((resolve, reject) => {
      const child = spawn(launch.command, launch.args, {
        cwd: config.extensionPath,
        env: launch.env,
        windowsHide: true,
      });

      let stdout = "";
      let stderr = "";

      child.stdout.on("data", (chunk: Buffer) => {
        const text = chunk.toString();
        stdout += text;
        this.output.append(text);
      });
      child.stderr.on("data", (chunk: Buffer) => {
        const text = chunk.toString();
        stderr += text;
        this.output.append(text);
      });
      child.on("error", reject);
      child.on("close", (code) => {
        if (code === 0) {
          resolve(stdout.trim());
          return;
        }
        reject(new Error(stderr.trim() || `Agent Warden scan failed with code ${code}`));
      });
    });
  }
}
