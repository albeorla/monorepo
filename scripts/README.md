# Development Scripts

This directory contains utility scripts to assist with development tasks.

## Python Virtual Environment

### Setting Up a Virtual Environment

To create a virtual environment that mirrors the project's dependencies:

```bash
# Generate requirements_lock.txt from Bazel dependencies
./scripts/generate_requirements.sh

# Create and populate a virtual environment
./scripts/setup_venv.sh

# Activate the virtual environment
source .venv/bin/activate
```

The virtual environment will include all dependencies required for development, testing, and linting of Python modules in this repository.

### Benefits

Using a virtual environment provides several advantages:

1. **IDE Integration**: Better IDE code completion and type checking
2. **Local Testing**: Run tests without invoking Bazel for faster iteration
3. **Dependency Management**: Clear view of exactly which package versions are being used

### Maintenance

When dependencies change in the Bazel build files, regenerate the requirements file:

```bash
./scripts/generate_requirements.sh
./scripts/setup_venv.sh  # Update existing venv
```

## CI Testing

To test GitHub Actions workflows locally:

1. Install Act: `brew install act` (macOS) or follow [Act installation guide](https://github.com/nektos/act#installation)
2. Run the workflow: `act -W .github/workflows/python-ci-test.yml -j python-lint`

See `.github/TESTING_CI.md` for more details on how to test workflows locally.