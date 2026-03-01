# ProxyPin MCP Server

![NPM Version](https://img.shields.io/npm/v/proxypin-mcp.svg) ![GitHub License](https://img.shields.io/github/license/ElonJask/proxypin-mcp.svg) ![Stars](https://img.shields.io/github/stars/ElonJask/proxypin-mcp.svg) [![MCP Badge](https://lobehub.com/badge/mcp/elonjask-proxypin-mcp?style=flat)](https://lobehub.com/mcp/elonjask-proxypin-mcp)

ProxyPin MCP Server 基于 Model Context Protocol (MCP)，配合开源项目 [ProxyPin](https://github.com/wanghongenpin/proxypin) 使用，将本地抓包历史提供给 MCP 客户端。

文档切换：[English](README.md) | [中文](README_CN.md)

## 功能特性

- 读取本地 ProxyPin 历史（HAR）
- 列表/搜索/详情等工具
- API 结构分析与调用代码生成
- 兼容主流 MCP 客户端（Windsurf / Cursor / Claude Desktop / Codex）

## 使用前

1. 安装并打开 ProxyPin
2. 在 ProxyPin 的“历史”设置中开启“缓存日期”（必须）
3. 确保已有抓包历史数据
4. 安装 Node.js（用于 `npx`）与 `uv`（启动器支持 `uvx` 和 `uv tool run`）

## 安装方式

### npx 启动

```bash
npx -y proxypin-mcp@latest
```

NPX 启动桥接会优先尝试 `uvx`，不可用时自动回退到 `uv tool run`。

## 使用方法

在 MCP 客户端配置中添加：

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
> 若客户端不支持 `type` 字段，请删除该字段。

## 环境变量

| 变量 | 说明 | 默认值 |
|---|---|---|
| `PROXYPIN_DATA_DIR` | ProxyPin 历史目录 | 自动探测 |
| `PROXYPIN_HAR_LIMIT` | 最多扫描 HAR 文件数 | `50` |
| `PROXYPIN_MAX_BODY_SIZE` | Body 最大保留字节数 | `102400` |

## 可用工具

### list_requests

列出最近请求。

参数：
- `limit` (int, 可选, 默认 20)
- `detail` (string: `summary` | `key` | `full`)
- `domain` (string, 可选)
- `method` (string, 可选)
- `status` (int, 可选)

### get_request

根据 ID 获取单条请求详情。

参数：
- `request_id` (string, 必填)
- `include_body` (boolean, 可选, 默认 true)

### search_requests

按关键词搜索请求。

参数：
- `keyword` (string, 必填)
- `search_in` (string: `all` | `url` | `request_body` | `response_body`)
- `limit` (int, 可选, 默认 20)

### analyze_api

按域名分析 API 结构。

参数：
- `domain` (string, 必填)

### get_domains

列出抓包域名及统计。

参数：
- 无

### generate_code

从抓包请求生成调用代码。

参数：
- `request_id` (string, 必填)
- `language` (string: `python` | `javascript` | `typescript` | `curl`)
- `framework` (string: `requests` | `httpx` | `fetch` | `axios`)

## Skills（工具）

- `list_requests`：按条件列出最近 HTTP 请求。
- `get_request`：按请求 ID 获取单条详情。
- `search_requests`：按关键字检索 URL/请求体/响应体。
- `analyze_api`：按域名聚合 API 路径与状态分布。
- `get_domains`：统计抓包域名与请求方法。
- `generate_code`：从抓包生成 Python/JS/cURL 调用代码。

## Prompts（提示词）

- `analyze_api_prompt(domain)`：指导 API 结构分析流程。
- `debug_request_prompt(request_id)`：指导单次请求排障流程。

## Resources（资源）

- `proxypin://requests/recent`：最近请求摘要数据。
- `proxypin://domains`：域名统计摘要数据。

## License

本项目使用 [MIT](./LICENSE) 许可证。
