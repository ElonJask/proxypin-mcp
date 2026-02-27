# ProxyPin MCP [English](README.md) | 中文

## ProxyPin MCP 服务（配合 https://github.com/wanghongenpin/proxypin）

将本地 ProxyPin 抓包历史暴露给 MCP 客户端（Windsurf / Cursor / Claude Desktop / Codex）。

前置条件：在 ProxyPin 的“历史”中开启“缓存日期”，并确保已有抓包历史数据。

## 核心特性

- 本地读取 ProxyPin 历史抓包（HAR）
- MCP 工具：`list_requests` / `get_request` / `search_requests` / `analyze_api` / `get_domains` / `generate_code`
- 支持主流 MCP 客户端

## 赞助

- 如果有帮助，欢迎 Star 或提 Issue / PR

## 下载地址

### 启动方式（npx）

```bash
npx -y @elonjask/proxypin-mcp@latest
```

说明：该 npx 包为启动器，会调用 `uvx --from proxypin-mcp proxypin-mcp`，因此需要本机已安装 `uv`。

### MCP 配置（npx）

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
