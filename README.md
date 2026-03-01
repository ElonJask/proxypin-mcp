# ProxyPin MCP Server

![NPM Version](https://img.shields.io/npm/v/proxypin-mcp.svg) ![GitHub License](https://img.shields.io/github/license/ElonJask/proxypin-mcp.svg) ![Stars](https://img.shields.io/github/stars/ElonJask/proxypin-mcp.svg) [![MCP Badge](https://lobehub.com/badge/mcp/elonjask-proxypin-mcp?style=flat)](https://lobehub.com/mcp/elonjask-proxypin-mcp)

ProxyPin MCP Server is based on the Model Context Protocol (MCP). It works with the open source project [ProxyPin](https://github.com/wanghongenpin/proxypin) to expose your local capture history to MCP-capable clients.

Docs: [English](README.md) | [中文](README_CN.md)

## Features

- Read local ProxyPin history (HAR)
- List/search/detail tools for captured requests
- API structure analysis and code generation
- Works with mainstream MCP clients (Windsurf / Cursor / Claude Desktop / Codex)

## Prerequisites

1. Install and open ProxyPin
2. In ProxyPin History settings, enable “Cache Date” (required)
3. Ensure some capture history exists
4. Node.js (for `npx`) and `uv` (launcher supports both `uvx` and `uv tool run`)

## Installation

### Run with npx

```bash
npx -y proxypin-mcp@latest
```

The NPX bridge tries `uvx` first, then automatically falls back to `uv tool run`.

## Usage

Add the following configuration to your MCP client configuration file:

```json
{
  "mcpServers": {
    "proxypin": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "proxypin-mcp@latest"]
    }
  }
}
```

> [!TIP]
> If your client does not support `type`, remove the field.

## Environment Variables

| Variable | Description | Default |
|---|---|---|
| `PROXYPIN_DATA_DIR` | ProxyPin history directory | auto-detect |
| `PROXYPIN_HAR_LIMIT` | max HAR files scanned | `50` |
| `PROXYPIN_MAX_BODY_SIZE` | max body bytes kept | `102400` |

## Available Tools

### list_requests

List recent captured requests.

Parameters:
- `limit` (int, optional, default 20)
- `detail` (string: `summary` | `key` | `full`)
- `domain` (string, optional)
- `method` (string, optional)
- `status` (int, optional)

### get_request

Get a single request detail by ID.

Parameters:
- `request_id` (string, required)
- `include_body` (boolean, optional, default true)

### search_requests

Search requests by keyword.

Parameters:
- `keyword` (string, required)
- `search_in` (string: `all` | `url` | `request_body` | `response_body`)
- `limit` (int, optional, default 20)

### analyze_api

Analyze API structure for a domain.

Parameters:
- `domain` (string, required)

### get_domains

List captured domains with counts.

Parameters:
- none

### generate_code

Generate API call code from a captured request.

Parameters:
- `request_id` (string, required)
- `language` (string: `python` | `javascript` | `typescript` | `curl`)
- `framework` (string: `requests` | `httpx` | `fetch` | `axios`)

## Skills (Tools)

- `list_requests`: list recent HTTP requests with filters.
- `get_request`: fetch one request by ID.
- `search_requests`: keyword search across URL and body.
- `analyze_api`: group endpoint patterns for one domain.
- `get_domains`: summarize captured domains and method counts.
- `generate_code`: generate Python/JS/cURL snippets from a capture.

## Prompts

- `analyze_api_prompt(domain)`: guide API structure analysis workflow.
- `debug_request_prompt(request_id)`: guide request debugging workflow.

## Resources

- `proxypin://requests/recent`: recent request summary dataset.
- `proxypin://domains`: captured domains summary dataset.

## License

This project is licensed under the [MIT](./LICENSE) License.
