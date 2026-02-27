# ProxyPin MCP (npx launcher)

A lightweight npx launcher for `proxypin-mcp` (Python MCP server).

## Core Features

- Start the real server via `uvx --from proxypin-mcp proxypin-mcp`
- Provide `npx`-style configuration for MCP clients

## Download

### Run (npx)

```bash
npx -y @elonjask/proxypin-mcp@latest
```

### MCP config (npx)

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

### Notes

- `uv` must be installed (provides `uvx`)
- `proxypin-mcp` must exist on PyPI

## License

MIT
