# Bazel Monorepo Starter Kit

Cost–efficient, polyglot build system for Python, TypeScript, (optional) Go and Rust.

See `docs/PRD.md` for full requirements.

## Quick start

```bash
# install Bazelisk, Python 3.11, Node 18, optionally Go 1.22 and Rust 1.78
bazel fetch //...
bazel run //python/hello_python
```

For full docs, open the PRD.

## Local Python development

We run everything through **Bazel**, but a small `.venv` makes IDEs and CLI
tools (ruff, pytest) snappy.

```bash
# one‑time setup
./scripts/setup_venv.sh          # creates .venv & installs pinned deps

# daily workflow
source .venv/bin/activate        # enable auto‑complete, etc.
ruff check python/               # or pre‑commit run --all-files
pytest -q python/…               # fast unit loop

# canonical build / test
bazel test //python/...          # or bazel run //python/todost:todost
```

`requirements_lock.txt` is the **single source of truth** for package
versions.  The Bazel `pip.parse()` extension vendors those wheels under
repositories such as `@pypi__httpx//:pkg`, while the setup script installs the
same versions into your venv.  Edit the lock file only when you purposefully
add or bump a dependency.
