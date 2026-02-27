# ProxyPin MCP (npx launcher)

A lightweight npx launcher for `proxypin-mcp` (Python MCP server). This package only starts the real server.

Language: English | 中文 see `README_CN.md` (if you want, I can add it)

## Overview

This package is a thin wrapper that runs:

```bash
uvx --from proxypin-mcp proxypin-mcp
```

It is meant for MCP clients that prefer `npx`-style configuration.

## Quick Start

```bash
npx -y @elonjask/proxypin-mcp@latest
```

## MCP Client Config

```json
{
  "mcpServers": {
    "proxypin": {
      "command": "npx",
      "args": ["-y", "@elonjask/proxypin-mcp@latest"]
    }
  }
}
```

## Requirements

- `uv` installed (provides `uvx`)
- `proxypin-mcp` published on PyPI

## Notes

- This package does not bundle the Python server.
- Use it only as a launcher.

## License

MIT
