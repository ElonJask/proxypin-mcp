#!/usr/bin/env node
"use strict";

const { spawn, spawnSync } = require("node:child_process");

function hasCommand(command) {
  const result = spawnSync(command, ["--version"], { stdio: "ignore" });
  return !result.error && result.status === 0;
}

function start(command, args) {
  const child = spawn(command, args, { stdio: "inherit", env: process.env });
  child.on("exit", (code) => process.exit(code ?? 1));
  child.on("error", (err) => {
    console.error(`[proxypin-mcp] failed to start ${command}: ${err.message}`);
    process.exit(1);
  });
}

const passthroughArgs = process.argv.slice(2);

if (hasCommand("uvx")) {
  start("uvx", ["--from", "proxypin-mcp", "proxypin-mcp", ...passthroughArgs]);
} else if (hasCommand("uv")) {
  start("uv", ["tool", "run", "--from", "proxypin-mcp", "proxypin-mcp", ...passthroughArgs]);
} else {
  console.error("[proxypin-mcp] `uv` (or `uvx`) is required but was not found in PATH.");
  console.error(
    "[proxypin-mcp] Install uv first: https://docs.astral.sh/uv/getting-started/installation/"
  );
  process.exit(1);
}
