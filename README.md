# ProxyPin MCP

ProxyPin MCP server for local capture history, designed to work with ProxyPin ([wanghongenpin/proxypin](https://github.com/wanghongenpin/proxypin)).

Language: [English](README.md) | [中文](README_CN.md)

## Open-source MCP for ProxyPin

Expose local ProxyPin history to MCP-capable clients (Windsurf / Cursor / Claude Desktop / Codex).

## Core Features

- Read local ProxyPin history (HAR)
- Token-efficient tools for list/search/detail
- API structure analysis and code generation
- Works with mainstream MCP clients

## Sponsor

- Star the repo or open an issue/PR if this helps

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

- Enable “Cache Date” in ProxyPin History (required)
- Ensure some capture history exists
- `uv` must be installed (the launcher calls `uvx --from proxypin-mcp proxypin-mcp`)

## License

MIT
