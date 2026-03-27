# Contributing to drt

Thank you for your interest in contributing!

## Development Setup

```bash
git clone https://github.com/drt-hub/drt.git
cd drt
uv pip install -e ".[dev,bigquery]"
```

## Running Tests

```bash
make test       # run all tests
make lint       # ruff + mypy
make fmt        # auto-format
```

## Submitting Changes

1. Fork the repository
2. Create a branch: `git checkout -b feat/your-feature`
3. Make your changes with tests
4. Run `make lint` and `make test`
5. Open a Pull Request

## Commit Style

Use [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add Snowflake source
fix: handle empty batch in REST API destination
docs: update quickstart example
```

## Adding a Connector

See `drt/sources/base.py` and `drt/destinations/base.py` for the Protocol interfaces.
Implement the protocol, add tests under `tests/`, and add an example under `examples/`.

## Code of Conduct

Be kind, be constructive. We follow the [Contributor Covenant](https://www.contributor-covenant.org/).
