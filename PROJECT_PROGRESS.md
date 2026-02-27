# Project Progress

## 2026-02-27

### Scope

Pre-open-source hardening and standardization for `proxypin-mcp`.

### Completed

- Removed high-risk scripts that exposed real credentials and non-public offensive security content.
- Added repository governance files:
  - `CONTRIBUTING.md`
  - `SECURITY.md`
  - `CODE_OF_CONDUCT.md`
  - `CHANGELOG.md`
  - `RELEASE_CHECKLIST.md`
- Added engineering baseline:
  - `.editorconfig`
  - `.pre-commit-config.yaml`
  - `.github/workflows/ci.yml`
  - `.github/workflows/codeql.yml`
  - `.github/dependabot.yml`
- Hardened core code:
  - environment variable parsing with range checks and fallback
  - line-by-line HAR parsing and stable fallback request IDs
  - safer and validated server tool inputs
  - more robust generated client code snippets
- Added tests for:
  - config fallback behavior
  - HAR reader ID/search behavior
  - server input validation behavior
- Added zero-install MCP usage docs and examples:
  - `uvx proxypin-mcp` for registry-distributed usage
  - `uv --directory <repo> run proxypin-mcp` for local checkout usage without `pip install`
- Added automated publish workflow:
  - `.github/workflows/publish.yml` for tag-triggered PyPI publishing via trusted publisher
- Updated package metadata:
  - maintainer identity and repository URLs in `pyproject.toml`
- Updated README to a simpler, ProxyPin-style usage flow and documented the required history cache setting.
- Added an `npx` configuration example for MCP clients.

### Pending

- Replace placeholder security contact email with maintainer-owned mailbox.
- Run full checks in a clean environment and capture CI badge/status.
- Confirm final repository naming, topics, and GitHub metadata.
