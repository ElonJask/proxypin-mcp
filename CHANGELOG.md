# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog and this project follows Semantic Versioning.

## [Unreleased]

### Added

- Open-source governance files: `CONTRIBUTING.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`.
- CI workflow with lint, type check, and tests.
- Security automation: `CodeQL` workflow and `Dependabot` configuration.
- Initial test suite for config parsing, HAR reader behavior, and server tool validation.
- Pre-commit and editor configuration.
- Zero-install MCP integration guidance and examples (`uvx` and `uv --directory ... run`).
- Automated publishing workflow for PyPI (`.github/workflows/publish.yml`).
- Simplified README and added `npx` launcher instructions + example.
- Aligned README structure to ProxyPin style and split into English/Chinese docs.
- Rewrote README to follow markmap-mcp-server style with detailed sections.
- Set security contact email and removed `uv.lock` from the repo.
- Added explicit MCP capability sections in README (`Skills`, `Prompts`, `Resources`) for easier registry verification.

### Changed

- Hardened configuration parsing for environment variables.
- Improved HAR parsing robustness and stable auto-generated request IDs.
- Improved tool input validation and code generation output reliability.
- Updated package metadata for open-source publishing (author and repository URLs).
- Renamed npm launcher package from `@elonjask/proxypin-mcp` to `proxypin-mcp` and updated all MCP config examples accordingly.
- Updated NPX launcher to prefer `uvx` and fallback to `uv tool run` when `uvx` is unavailable.
- Bumped versions to `0.1.1` (Python package and npm bridge).

### Removed

- Sensitive, non-open-source-ready scripts containing hard-coded credentials and offensive testing payloads.
- CodeQL workflow and Dependabot config (stop automated security scanning/PR noise).
- Unpublished npm package `@elonjask/proxypin-mcp` after successful migration to `proxypin-mcp`.
