# ProxyPin MCP

ProxyPin MCP server for local capture history, designed to work with ProxyPin (https://github.com/wanghongenpin/proxypin).

Language: English | 中文 see `README_CN.md`

## Overview

ProxyPin MCP exposes your local ProxyPin history to MCP-capable clients (Windsurf / Cursor / Claude Desktop / Codex). It runs on your machine and reads local HAR history files.

## Features

- Read ProxyPin local history (HAR)
- Token-efficient tools for list/search/detail
- API structure analysis and code generation
- Works with mainstream MCP clients

## Prerequisites

- Install and open ProxyPin
- In ProxyPin History settings, enable “Cache Date” (required)
- Ensure some capture history exists

## Quick Start (npx)

```bash
npx -y @elonjask/proxypin-mcp@latest
```

Requirement: `uv` must be installed (the launcher calls `uvx --from proxypin-mcp proxypin-mcp`).

## MCP Client Config (npx)

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

## Tools

- `list_requests`: list recent requests
- `get_request`: get single request detail
- `search_requests`: search in URL/body
- `analyze_api`: aggregate endpoint patterns
- `get_domains`: list captured domains
- `generate_code`: generate Python/JS/cURL snippet

## Environment Variables

| Variable | Description | Default |
|---|---|---|
| `PROXYPIN_DATA_DIR` | ProxyPin history directory | auto-detect |
| `PROXYPIN_HAR_LIMIT` | max HAR files scanned | `50` |
| `PROXYPIN_MAX_BODY_SIZE` | max body bytes kept | `102400` |

## FAQ

- No data returned?
Enable “Cache Date” in ProxyPin History, then generate new traffic. Also check `PROXYPIN_DATA_DIR`.

- Do I need to install Python?
The npx launcher uses `uvx` under the hood. Install `uv` once and you are done.

## Security Notice

- Never commit real captures with tokens/cookies/personal data.
- Never commit credentials in scripts or docs.
- Use environment variables for secrets.

## Related Project

- ProxyPin: https://github.com/wanghongenpin/proxypin

## License

MIT
