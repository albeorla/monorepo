# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build Commands
- Build/run: `bazel run //path/to/target` (e.g., `bazel run //python/hello_python`)
- Test all: `bazel test //...`
- Integration tests: `bazel test --test_tag_filters=integ`
- Format code: Use pre-commit hooks (`pre-commit run --all-files`)
- Lint TypeScript: `cd ts && npx eslint .`
- Lint Python: `ruff check`

## Code Style
- **TypeScript**: Follow ESLint config - imports ordered (builtin→external→internal→parent→sibling→index) with newlines between groups
- **Python**: Follow Ruff rules (PEP8 + additional checks) with 88-char line length
- **Bazel**: Use buildifier for formatting
- **Naming**: snake_case for Python, camelCase for TypeScript; unused vars prefixed with underscore
- **Errors**: Avoid console.log (only warn/error); add type annotations
- **Features**: Go/Rust are optional (use `--//features:go` or `--//features:rust` flags)

## Cost Efficiency
- CI cost per PR must be ≤ $0.10
- Keep build times under 60 seconds when possible