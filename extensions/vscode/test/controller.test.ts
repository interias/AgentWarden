import * as assert from "assert";
import test from "node:test";

import { statusFromProcessClose } from "../src/controller";

test("statusFromProcessClose treats intentional stop as stopped", () => {
  assert.equal(statusFromProcessClose(true, null), "stopped");
});

test("statusFromProcessClose treats zero exit as stopped", () => {
  assert.equal(statusFromProcessClose(false, 0), "stopped");
});

test("statusFromProcessClose treats unexpected nonzero exit as error", () => {
  assert.equal(statusFromProcessClose(false, 1), "error");
});
