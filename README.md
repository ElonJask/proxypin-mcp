# ProxyPin MCP Server

[English](#english) | [中文](#中文)

MCP (Model Context Protocol) server for [ProxyPin](https://github.com/wanghongenpin/proxypin), exposing captured HTTP data to AI tools (Windsurf, Cursor, Claude Desktop, etc.).

---

## English

### Features

- Cross-platform: macOS, Windows, Linux
- Token-efficient detail levels: `summary` / `key` / `full`
- Request/response visibility: headers, body, timing, app metadata
- Helper tooling: API analysis, request search, client-code generation

### Installation

```bash
# with uv (recommended)
uv pip install proxypin-mcp

# or with pip
pip install proxypin-mcp
```

### MCP Client Configuration

Use the same config for Windsurf/Cursor/Claude Desktop:

#### Option A: installed Python environment

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

#### Option B: zero-install from package registry (recommended for end users)

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

Requirements:
- `proxypin-mcp` has been published to PyPI.
- `uv` is installed on the target machine.

#### Option C: zero-install from a local checkout (no `pip install`)

```json
{
  "mcpServers": {
    "proxypin": {
      "command": "uv",
      "args": [
        "--directory",
        "/ABSOLUTE/PATH/TO/proxypin-mcp",
        "run",
        "proxypin-mcp"
      ]
    }
  }
}
```

### Tools

| Tool | Description |
|------|-------------|
| `list_requests` | List recent requests with filters |
| `get_request` | Get single request detail |
| `search_requests` | Search in URL/body |
| `analyze_api` | Aggregate endpoint patterns |
| `get_domains` | List captured domains |
| `generate_code` | Generate Python/JS/cURL snippet |

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `PROXYPIN_DATA_DIR` | ProxyPin history directory | auto-detect |
| `PROXYPIN_HAR_LIMIT` | max HAR files scanned | `50` |
| `PROXYPIN_MAX_BODY_SIZE` | max body bytes kept | `102400` |

### Development

```bash
git clone https://github.com/ElonJask/proxypin-mcp.git
cd proxypin-mcp
pip install -e ".[dev]"

# run server
python -m proxypin_mcp

# quality gates
ruff check .
ruff format --check .
mypy src
pytest
```

### Open-Source Governance

- Contribution guide: [CONTRIBUTING.md](CONTRIBUTING.md)
- Security policy: [SECURITY.md](SECURITY.md)
- Code of conduct: [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)
- Changelog: [CHANGELOG.md](CHANGELOG.md)
- Release checklist: [RELEASE_CHECKLIST.md](RELEASE_CHECKLIST.md)
- Project progress log: [PROJECT_PROGRESS.md](PROJECT_PROGRESS.md)

### Security Notice

- Never commit real captures containing tokens, cookies, or personal data.
- Never commit credentials in scripts/docs.
- Use environment variables for all secrets.

---

## 中文

ProxyPin 的 MCP 服务，将抓包数据提供给 AI 工具（Windsurf / Cursor / Claude Desktop 等）进行分析与开发辅助。

### 特性

- 跨平台：macOS / Windows / Linux
- Token 友好：`summary` / `key` / `full` 三级详情
- 数据完整：请求响应头、Body、耗时、应用信息
- 能力完整：搜索、API 结构分析、代码生成

### 安装

```bash
uv pip install proxypin-mcp
# 或
pip install proxypin-mcp
```

### MCP 配置

Windsurf / Cursor / Claude Desktop 都可以使用：

#### 方案 A：已安装 Python 环境

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

#### 方案 B：通过包仓库零安装运行（推荐给最终用户）

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

要求：
- `proxypin-mcp` 已发布到 PyPI。
- 目标机器已安装 `uv`。

#### 方案 C：本地源码目录零安装运行（无需 `pip install`）

```json
{
  "mcpServers": {
    "proxypin": {
      "command": "uv",
      "args": [
        "--directory",
        "/ABSOLUTE/PATH/TO/proxypin-mcp",
        "run",
        "proxypin-mcp"
      ]
    }
  }
}
```

### 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `PROXYPIN_DATA_DIR` | ProxyPin 历史目录 | 自动探测 |
| `PROXYPIN_HAR_LIMIT` | 最多扫描 HAR 文件数 | `50` |
| `PROXYPIN_MAX_BODY_SIZE` | Body 最大保留字节数 | `102400` |

### 开发与质量门禁

```bash
git clone https://github.com/ElonJask/proxypin-mcp.git
cd proxypin-mcp
pip install -e ".[dev]"

python -m proxypin_mcp

ruff check .
ruff format --check .
mypy src
pytest
```

### 开源协作规范

- 贡献指南：[CONTRIBUTING.md](CONTRIBUTING.md)
- 安全策略：[SECURITY.md](SECURITY.md)
- 行为准则：[CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)
- 变更记录：[CHANGELOG.md](CHANGELOG.md)
- 发布清单：[RELEASE_CHECKLIST.md](RELEASE_CHECKLIST.md)
- 项目进展：[PROJECT_PROGRESS.md](PROJECT_PROGRESS.md)

### 安全声明

- 禁止提交包含 Token/Cookie/隐私数据的真实抓包文件。
- 禁止提交明文凭据或生产配置。
- 所有敏感信息必须通过环境变量注入。

---

## License

MIT
