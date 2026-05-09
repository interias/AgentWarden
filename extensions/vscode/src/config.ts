import * as fs from "fs";
import * as path from "path";

export const POSITIONS = ["top-left", "top-right", "bottom-left", "bottom-right"] as const;
export type OverlayPosition = (typeof POSITIONS)[number];

export interface SettingReader {
  get<T>(key: string, defaultValue: T): T;
}

export interface AgentWardenConfig {
  position: OverlayPosition;
  pollIntervalSeconds: number;
  activeThresholdSeconds: number;
  opacity: number;
  sessionsRoot: string;
  pythonPath: string;
  autoStart: boolean;
  extensionPath: string;
  pythonPackageRoot: string;
}

export interface LaunchSpec {
  command: string;
  args: string[];
  env: NodeJS.ProcessEnv;
}

export function resolveAgentWardenConfig(reader: SettingReader, extensionPath: string): AgentWardenConfig {
  const position = normalizePosition(reader.get("position", "top-right"));
  const pollIntervalSeconds = normalizeNumber(
    reader.get("pollIntervalSeconds", 10),
    "pollIntervalSeconds",
    5,
    60,
  );
  const activeThresholdSeconds = normalizeNumber(
    reader.get("activeThresholdSeconds", 60),
    "activeThresholdSeconds",
    1,
  );
  const opacity = normalizeNumber(reader.get("opacity", 0.92), "opacity", 0.2, 1);

  return {
    position,
    pollIntervalSeconds,
    activeThresholdSeconds,
    opacity,
    sessionsRoot: reader.get("sessionsRoot", "").trim(),
    pythonPath: reader.get("pythonPath", "").trim(),
    autoStart: reader.get("autoStart", false),
    extensionPath,
    pythonPackageRoot: resolvePythonPackageRoot(extensionPath),
  };
}

export function buildLaunchSpec(
  config: AgentWardenConfig,
  once: boolean,
  baseEnv: NodeJS.ProcessEnv = process.env,
): LaunchSpec {
  const command = config.pythonPath || defaultPythonCommand();
  const args = [...defaultPythonArgs(command), "-m", "agent_warden"];

  args.push("--poll-interval", String(config.pollIntervalSeconds));
  args.push("--active-threshold", String(config.activeThresholdSeconds));
  args.push("--opacity", String(config.opacity));
  args.push("--position", config.position);

  if (config.sessionsRoot) {
    args.push("--sessions-root", config.sessionsRoot);
  }

  if (once) {
    args.push("--once");
  }

  return {
    command,
    args,
    env: buildPythonEnvironment(config.pythonPackageRoot, baseEnv),
  };
}

export function resolvePythonPackageRoot(extensionPath: string): string {
  const bundledRoot = path.join(extensionPath, "python");
  if (fs.existsSync(path.join(bundledRoot, "agent_warden"))) {
    return bundledRoot;
  }

  return path.resolve(extensionPath, "..", "..", "src");
}

export function buildPythonEnvironment(
  pythonPackageRoot: string,
  baseEnv: NodeJS.ProcessEnv = process.env,
): NodeJS.ProcessEnv {
  const env = { ...baseEnv };
  const existingPath = env.PYTHONPATH;
  env.PYTHONPATH = existingPath
    ? `${pythonPackageRoot}${path.delimiter}${existingPath}`
    : pythonPackageRoot;
  return env;
}

export function normalizePosition(value: string): OverlayPosition {
  const normalized = value.toLowerCase().replace("_", "-");
  if (POSITIONS.includes(normalized as OverlayPosition)) {
    return normalized as OverlayPosition;
  }
  throw new Error(`Invalid agentWarden.position: ${value}`);
}

function normalizeNumber(value: number, name: string, min: number, max?: number): number {
  const parsed = Number(value);
  if (!Number.isFinite(parsed) || parsed < min || (max !== undefined && parsed > max)) {
    const maxText = max === undefined ? "" : ` and at most ${max}`;
    throw new Error(`agentWarden.${name} must be at least ${min}${maxText}`);
  }
  return parsed;
}

function defaultPythonCommand(): string {
  return process.platform === "win32" ? "py" : "python3";
}

function defaultPythonArgs(command: string): string[] {
  return command === "py" ? ["-3"] : [];
}
