# ProxyPin MCP [English] | [中文](README_CN.md)

## MCP server for ProxyPin (https://github.com/wanghongenpin/proxypin)

Expose local ProxyPin capture history to MCP-capable clients (Windsurf / Cursor / Claude Desktop / Codex).

Prerequisite: enable “Cache Date” in ProxyPin History settings, and make sure some history exists.

## Core Features

- Read ProxyPin history (HAR) locally
- MCP tools: `list_requests`, `get_request`, `search_requests`, `analyze_api`, `get_domains`, `generate_code`
- Works with mainstream MCP clients

## Support

- Star the repo or open an issue/PR if this helps

## Download

### Run (npx)

```bash
npx -y @elonjask/proxypin-mcp@latest
```

Requirement: `uv` must be installed (the launcher calls `uvx --from proxypin-mcp proxypin-mcp`).

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

---

## License

MIT
