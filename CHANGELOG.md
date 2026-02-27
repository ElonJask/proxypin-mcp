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

### Changed

- Hardened configuration parsing for environment variables.
- Improved HAR parsing robustness and stable auto-generated request IDs.
- Improved tool input validation and code generation output reliability.
- Updated package metadata for open-source publishing (author and repository URLs).

### Removed

- Sensitive, non-open-source-ready scripts containing hard-coded credentials and offensive testing payloads.
