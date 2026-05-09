const fs = require("fs");
const path = require("path");

const extensionRoot = path.resolve(__dirname, "..");

for (const relativePath of ["out", "python"]) {
  fs.rmSync(path.join(extensionRoot, relativePath), { recursive: true, force: true });
}
