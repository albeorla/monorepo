# Python Module Scaffolding

This document describes the Python module scaffolding system for the monorepo.

## Overview

The Python scaffolding tools help you quickly create new Python modules with a consistent structure, following the monorepo's conventions and best practices. Each scaffolded module includes:

- Properly configured Bazel build targets
- Test setup
- Documentation template
- Type annotations and docstrings
- Proper directory structure

## Quick Start

To create a new Python module, run:

```bash
./scaffolding/scaffold_python.sh <module_name> [description] [author]
```

For example:
```bash
./scaffolding/scaffold_python.sh data_processor "Processes data files" "Data Team"
```

This will create a new module at `python/data_processor/` with all the necessary files.

## Module Structure

Each scaffolded module follows this structure:

```
python/module_name/
├── BUILD.bazel           # Bazel build configuration
├── __init__.py           # Package initialization
├── module_name.py        # Main module code
├── test_module_name.py   # Tests for the module
└── README.md             # Module documentation
```

## Customizing Templates

The scaffolding is based on templates located in:
```
scaffolding/python_cookiecutter/
```

You can modify these templates to adjust the generated code structure. The main template files are:

- `{{cookiecutter.module_name}}.py` - Main module code template
- `test_{{cookiecutter.module_name}}.py` - Test template
- `BUILD.bazel` - Bazel build configuration template
- `README.md` - Documentation template

## Configuration

The `cookiecutter.json` file defines parameters that can be used in templates:

```json
{
  "module_name": "my_python_module",
  "module_description": "A Python module in the monorepo",
  "author": "Monorepo Team",
  "with_tests": "yes",
  "include_cli": "yes"
}
```

## Best Practices

When creating a new module:

1. Choose clear, descriptive module names (lowercase with underscores)
2. Provide a concise but informative description
3. Update the README.md with specific usage information
4. Implement tests for all functionality
5. Follow PEP 8 style guidelines and use type hints

## Adding Functionality

If you need to add new functionality to the scaffolding system:

1. Update the templates in `scaffolding/python_cookiecutter/`
2. Add any new parameters to `cookiecutter.json` 
3. Update the `scaffold_python.sh` script to handle the new parameters
4. Document the changes in this README

## Related Documentation

- [PRD](../docs/PRD.md) - See sections F-5 for Python module requirements
- [CLAUDE.md](../CLAUDE.md) - Python coding conventions