# @elonjask/proxypin-mcp

NPX launcher package for `proxypin-mcp` (Python MCP server on PyPI).

## MCP config (Windsurf/Cursor/Claude Desktop)

```json
{
  "mcpServers": {
    "proxypin": {
      "command": "npx",
      "args": [
        "-y",
        "@elonjask/proxypin-mcp@latest"
      ]
    }
  }
}
```

## Runtime requirement

- `uv` must be installed on the local machine (`uvx` command available).

This package only launches:

```bash
uvx --from proxypin-mcp proxypin-mcp
```
