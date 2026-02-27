# Contributing

## Development Setup

1. Install Python 3.10+.
2. Create and activate a virtual environment.
3. Install dependencies:

```bash
pip install -e ".[dev]"
```

## Local Quality Gates

Run all checks before submitting PRs:

```bash
ruff check .
ruff format --check .
mypy src
pytest
```

## Pull Request Rules

- Keep PRs focused and small.
- Add tests for behavior changes.
- Update `CHANGELOG.md` under the `Unreleased` section.
- Never commit secrets, real production captures, or personal data.

## Commit Convention

Recommended style:

- `feat: ...`
- `fix: ...`
- `docs: ...`
- `chore: ...`
