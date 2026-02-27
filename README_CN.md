# ProxyPin MCP

ProxyPin MCP 服务（配合 [wanghongenpin/proxypin](https://github.com/wanghongenpin/proxypin) 使用），将本地抓包历史暴露给 MCP 客户端。

语言切换：[English](README.md) | [中文](README_CN.md)

## 开源免费 MCP 服务

面向 MCP 客户端（Windsurf / Cursor / Claude Desktop / Codex），读取本机 ProxyPin 抓包历史。

## 核心特性

- 读取本地 ProxyPin 历史（HAR）
- 支持列表/搜索/详情等工具
- API 结构分析与调用代码生成
- 兼容主流 MCP 客户端

## 赞助

- 如果有帮助，欢迎 Star 或提 Issue / PR

## 下载地址

### 启动方式（npx）

```bash
npx -y @elonjask/proxypin-mcp@latest
```

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

### 使用说明

- 在 ProxyPin 的“历史”设置中开启“缓存日期”（必须）
- 确保已有抓包历史数据
- 本机需已安装 `uv`（启动器会调用 `uvx --from proxypin-mcp proxypin-mcp`）

## License

MIT
