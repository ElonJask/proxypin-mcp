# Release Checklist

## Before Tagging

- [ ] `pip install -e ".[dev]"` succeeds
- [ ] `ruff check .` passes
- [ ] `ruff format --check .` passes
- [ ] `mypy src` passes
- [ ] `pytest` passes
- [ ] `CHANGELOG.md` updated
- [ ] `README.md` version/examples verified
- [ ] `SECURITY.md` contact email is real
- [ ] no secrets in git history and working tree

## Package Validation

- [ ] `python -m build` succeeds
- [ ] `twine check dist/*` passes
- [ ] test install from built wheel

## GitHub Release

- [ ] PyPI trusted publisher configured for `ElonJask/proxypin-mcp` (`.github/workflows/publish.yml`)
- [ ] create version tag (`vX.Y.Z`)
- [ ] publish GitHub release notes from changelog
- [ ] publish package to PyPI (if applicable)
