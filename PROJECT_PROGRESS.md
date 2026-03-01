# Project Progress

## 2026-03-01 (Patch Release Prep)

### Scope

Registry score remediation for verification, skills, and prompts visibility.

### Completed

- Hardened NPX launcher compatibility:
  - primary path: `uvx --from proxypin-mcp proxypin-mcp`
  - fallback path: `uv tool run --from proxypin-mcp proxypin-mcp`
- Added explicit MCP capability sections to docs:
  - `Skills (Tools)` in `README.md` and `README_CN.md`
  - `Prompts` in `README.md` and `README_CN.md`
  - `Resources` in `README.md` and `README_CN.md`
- Raised release versions for patch delivery:
  - Python package `proxypin-mcp`: `0.1.1`
  - npm bridge `proxypin-mcp`: `0.1.1`
- Pushed release commit to `main` and created release tag:
  - commit: `af36636`
  - tag: `v0.1.1`
- Triggered GitHub Actions publish workflow:
  - run: `https://github.com/ElonJask/proxypin-mcp/actions/runs/22535201781`

### Pending

- Resolve npm publish authentication on local machine (`ENEEDAUTH`).
- Fix PyPI Trusted Publisher mapping (`invalid-publisher` for `repo:ElonJask/proxypin-mcp:environment:pypi`).
- Re-run npm publish and re-dispatch PyPI publish after credentials/trusted publisher fix.
- Trigger/confirm registry rescans on MCP listing platforms.

## 2026-03-01

### Scope

Repository hygiene review and README badge optimization.

### Completed

- Added LobeHub MCP badge to top badge row in:
  - `README.md`
  - `README_CN.md`
- Audited tracked files for non-MCP artifacts:
  - confirmed `dist/` wheel/tar files exist locally but are not tracked by git
  - no unrelated binary/media artifacts found in tracked files
- Verified ignore rules include common local-only artifacts (`dist/`, `.venv/`, caches, lockfiles).

### Pending

- Optional: add dedicated "Badges" section in README if more ecosystem badges are added later.

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
- Aligned README sections with ProxyPin structure and split English/Chinese docs.
- Consolidated example configs to `npx` only.
- Rewrote README (EN/CN) to follow markmap-mcp-server style and add detailed sections.
- Set security contact email in `SECURITY.md`.
- Removed `uv.lock` from version control (kept in `.gitignore`).
- Disabled automated security scanning/PR noise:
  - removed `.github/workflows/codeql.yml`
  - removed `.github/dependabot.yml`

### Pending

- Replace placeholder security contact email with maintainer-owned mailbox.
- Run full checks in a clean environment and capture CI badge/status.
- Confirm final repository naming, topics, and GitHub metadata.

## 2026-02-28

### Scope

NPM package rename migration from scoped name to unscoped name.

### Completed

- Renamed npm bridge package from `@elonjask/proxypin-mcp` to `proxypin-mcp`.
- Updated installation and MCP config examples in:
  - `README.md`
  - `README_CN.md`
  - `npm-bridge/README.md`
  - `examples/*.json`
- Published new package: `proxypin-mcp@0.1.0`.
- Unpublished old scoped package: `@elonjask/proxypin-mcp` (registry now reports unpublished timestamp).

### Pending

- Optional: add deprecation notice/migration note in GitHub release notes for users who still reference old docs/screenshots.
