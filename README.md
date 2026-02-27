# ProxyPin MCP [English](#english) | 中文

ProxyPin 的 MCP 服务，把抓包历史数据提供给 AI 工具（Windsurf / Cursor / Claude Desktop / Codex）。

## 使用前

- 安装并打开 ProxyPin
- 在 ProxyPin 的“历史”选项中开启“缓存日期”（必须）
- 先产生一些抓包历史数据

## 快速开始（最简单）

### 方式 A：npx（你要的命令即用）

```bash
npx -y @elonjask/proxypin-mcp@latest
```

> 说明：该 npx 包是启动器，会调用 `uvx --from proxypin-mcp proxypin-mcp`，因此需要本机已安装 `uv`。

### 方式 B：uvx（Python 包零安装）

```bash
uvx proxypin-mcp
```

### 方式 C：已安装 Python 环境

```bash
pip install proxypin-mcp
python -m proxypin_mcp
```

## MCP 配置（Windsurf / Cursor / Claude Desktop / Codex）

选择你要的启动方式填入：

### npx 方式

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

### uvx 方式

```json
{
  "mcpServers": {
    "proxypin": {
      "command": "uvx",
      "args": ["proxypin-mcp"]
    }
  }
}
```

### python 方式

```json
{
  "mcpServers": {
    "proxypin": {
      "command": "python",
      "args": ["-m", "proxypin_mcp"]
    }
  }
}
```

## 核心能力

- `list_requests`：列出最近请求
- `get_request`：获取单条请求详情
- `search_requests`：按关键词搜索请求
- `analyze_api`：API 结构分析
- `get_domains`：列出抓包域名
- `generate_code`：生成 Python/JS/cURL 调用示例

## 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `PROXYPIN_DATA_DIR` | ProxyPin 历史目录 | 自动探测 |
| `PROXYPIN_HAR_LIMIT` | 最多扫描 HAR 文件数 | `50` |
| `PROXYPIN_MAX_BODY_SIZE` | Body 最大保留字节数 | `102400` |

## 安全声明

- 禁止提交包含 Token/Cookie/隐私数据的真实抓包文件。
- 禁止提交明文凭据或生产配置。
- 所有敏感信息必须通过环境变量注入。

---

## English

ProxyPin MCP server that exposes local ProxyPin capture history to MCP-capable clients.

### Prerequisites

- Install and open ProxyPin
- Enable “cache date” in ProxyPin history settings (required)
- Ensure some history data exists

### Quickstart

```bash
# npx launcher (requires uvx)
npx -y @elonjask/proxypin-mcp@latest

# or uvx
uvx proxypin-mcp
```

### MCP config

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

### Tools

- `list_requests`
- `get_request`
- `search_requests`
- `analyze_api`
- `get_domains`
- `generate_code`

---

## License

MIT
