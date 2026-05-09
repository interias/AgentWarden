import * as assert from "assert";
import * as fs from "fs";
import * as os from "os";
import * as path from "path";
import test from "node:test";

import {
  buildLaunchSpec,
  buildPythonEnvironment,
  normalizePosition,
  resolveAgentWardenConfig,
  resolvePythonPackageRoot,
  SettingReader,
} from "../src/config";

class MapReader implements SettingReader {
  constructor(private readonly values: Record<string, unknown>) {}

  get<T>(key: string, defaultValue: T): T {
    return (this.values[key] ?? defaultValue) as T;
  }
}

test("resolveAgentWardenConfig applies defaults", () => {
  const config = resolveAgentWardenConfig(new MapReader({}), path.join("repo", "extensions", "vscode"));

  assert.equal(config.position, "top-right");
  assert.equal(config.pollIntervalSeconds, 10);
  assert.equal(config.activeThresholdSeconds, 60);
  assert.equal(config.opacity, 0.92);
  assert.equal(config.sessionsRoot, "");
  assert.equal(config.pythonPath, "");
  assert.equal(config.autoStart, false);
});

test("normalizePosition accepts underscore aliases", () => {
  assert.equal(normalizePosition("bottom_right"), "bottom-right");
});

test("buildLaunchSpec includes overlay and scan arguments", () => {
  const config = resolveAgentWardenConfig(
    new MapReader({
      position: "bottom-left",
      pollIntervalSeconds: 5,
      activeThresholdSeconds: 30,
      opacity: 0.8,
      sessionsRoot: "C:\\Users\\you\\.codex\\sessions",
      pythonPath: "C:\\Python313\\python.exe",
    }),
    path.join("repo", "extensions", "vscode"),
  );

  const spec = buildLaunchSpec(config, true, {});

  assert.equal(spec.command, "C:\\Python313\\python.exe");
  assert.deepEqual(spec.args, [
    "-m",
    "agent_warden",
    "--poll-interval",
    "5",
    "--active-threshold",
    "30",
    "--opacity",
    "0.8",
    "--position",
    "bottom-left",
    "--sessions-root",
    "C:\\Users\\you\\.codex\\sessions",
    "--once",
  ]);
});

test("buildPythonEnvironment prepends package root", () => {
  const env = buildPythonEnvironment("C:\\agent-warden\\python", { PYTHONPATH: "C:\\existing" });

  assert.equal(env.PYTHONPATH, `C:\\agent-warden\\python${path.delimiter}C:\\existing`);
});

test("resolvePythonPackageRoot prefers bundled package", () => {
  const tempRoot = fs.mkdtempSync(path.join(os.tmpdir(), "agent-warden-extension-"));
  const bundledPackage = path.join(tempRoot, "python", "agent_warden");
  fs.mkdirSync(bundledPackage, { recursive: true });

  assert.equal(resolvePythonPackageRoot(tempRoot), path.join(tempRoot, "python"));
});
