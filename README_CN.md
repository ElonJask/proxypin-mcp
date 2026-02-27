# ProxyPin MCP

ProxyPin MCP 服务（配合 https://github.com/wanghongenpin/proxypin 使用），将本地抓包历史暴露给 MCP 客户端。

语言：中文 | English see `README.md`

## 简介

ProxyPin MCP 会读取本机 ProxyPin 的历史抓包（HAR），提供给 MCP 客户端（Windsurf / Cursor / Claude Desktop / Codex）。

## 核心特性

- 读取本地 ProxyPin 历史（HAR）
- 支持列表/搜索/详情等工具
- API 结构分析与调用代码生成
- 兼容主流 MCP 客户端

## 使用前

- 安装并打开 ProxyPin
- 在 ProxyPin 的“历史”设置中开启“缓存日期”（必须）
- 确保已有抓包历史数据

## 快速开始（npx）

```bash
npx -y @elonjask/proxypin-mcp@latest
```

说明：该 npx 包是启动器，会调用 `uvx --from proxypin-mcp proxypin-mcp`，需要本机已安装 `uv`。

## MCP 配置（npx）

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

## 工具列表

- `list_requests`：列出最近请求
- `get_request`：获取单条请求详情
- `search_requests`：按关键词搜索请求
- `analyze_api`：API 结构分析
- `get_domains`：列出抓包域名
- `generate_code`：生成 Python/JS/cURL 调用示例

## 环境变量

| 变量 | 说明 | 默认值 |
|---|---|---|
| `PROXYPIN_DATA_DIR` | ProxyPin 历史目录 | 自动探测 |
| `PROXYPIN_HAR_LIMIT` | 最多扫描 HAR 文件数 | `50` |
| `PROXYPIN_MAX_BODY_SIZE` | Body 最大保留字节数 | `102400` |

## 常见问题

- 没有数据？
请确认已在 ProxyPin 历史设置中开启“缓存日期”，并产生新的抓包数据；必要时设置 `PROXYPIN_DATA_DIR`。

- 是否需要安装 Python？
`npx` 启动器会调用 `uvx`，只需要安装一次 `uv` 即可。

## 安全声明

- 禁止提交包含 Token/Cookie/隐私数据的真实抓包文件。
- 禁止提交明文凭据或生产配置。
- 所有敏感信息必须通过环境变量注入。

## 相关项目

- ProxyPin：https://github.com/wanghongenpin/proxypin

## License

MIT
