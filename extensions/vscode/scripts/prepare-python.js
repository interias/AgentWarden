const fs = require("fs");
const path = require("path");

const extensionRoot = path.resolve(__dirname, "..");
const repoRoot = path.resolve(extensionRoot, "..", "..");
const sourceRoot = path.join(repoRoot, "src", "agent_warden");
const targetRoot = path.join(extensionRoot, "python", "agent_warden");

function copyDirectory(source, target) {
  fs.mkdirSync(target, { recursive: true });

  for (const entry of fs.readdirSync(source, { withFileTypes: true })) {
    if (entry.name === "__pycache__" || entry.name.endsWith(".pyc")) {
      continue;
    }

    const sourcePath = path.join(source, entry.name);
    const targetPath = path.join(target, entry.name);

    if (entry.isDirectory()) {
      copyDirectory(sourcePath, targetPath);
    } else if (entry.isFile()) {
      fs.copyFileSync(sourcePath, targetPath);
    }
  }
}

if (!fs.existsSync(sourceRoot)) {
  throw new Error(`Python source package not found: ${sourceRoot}`);
}

fs.rmSync(targetRoot, { recursive: true, force: true });
copyDirectory(sourceRoot, targetRoot);
console.log(`Copied Python package to ${targetRoot}`);
