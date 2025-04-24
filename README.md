# Bazel Monorepo Starter Kit (Updated: 2025-05-07)

Cost–efficient, polyglot build system for Python, TypeScript, (optional) Go and Rust with container support.

See `docs/PRD.md` for full requirements and project documentation.

## Documentation

- **Product Requirements**: [docs/PRD.md](docs/PRD.md)
- **Planning & Roadmap**: [docs/planning/](docs/planning/)
- **Technical Decisions**: [docs/decisions/](docs/decisions/)
- **Work Summaries**: [docs/reports/](docs/reports/)
- **Container Workflow**: [docs/container_workflow.md](docs/container_workflow.md)

## Quick start

```bash
# install Bazelisk, Python 3.11, Node 18, optionally Go 1.22 and Rust 1.78
bazel fetch //...
bazel run //python/hello_python

# Build and run container (requires Docker)
bazel run //python/hello_python:hello_python_image_load
docker run -it --rm localhost/hello_python
```

For full project documentation, see the [docs/](docs/) directory.

## Included Modules

### Python Modules

- **hello_python**: Simple "Hello World" example
- **todost**: Todoist → PARA+GTD exporter for productivity system integration
  ([documentation](python/todost/README.md))

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
