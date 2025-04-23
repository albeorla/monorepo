# {{cookiecutter.module_name}}

A Python module within the monorepo.

## Overview

Describe the purpose and functionality of this module.

## Usage

```bash
# Run using Bazel
bazel run //python/{{cookiecutter.module_name}}

# Test using Bazel 
bazel test //python/{{cookiecutter.module_name}}:{{cookiecutter.module_name}}_test
```

## API

### `process_data(data: Dict[str, Any]) -> List[Dict[str, Any]]`

Process input data and return transformed results.

## Development

1. Make your changes
2. Run tests: `pytest python/{{cookiecutter.module_name}}/test_{{cookiecutter.module_name}}.py`
3. Run linting: `ruff check python/{{cookiecutter.module_name}}/`