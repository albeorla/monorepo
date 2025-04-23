# Todoist → PARA+GTD Exporter

A Python module for exporting [Todoist](https://todoist.com/) tasks, projects, and sections to a structured JSON format following the PARA (Projects, Areas, Resources, Archives) method and GTD (Getting Things Done) principles.

## Features

- 🔄 Fetches data from Todoist REST API v2
- 🧠 Applies rule-based categorization using regex patterns and labels
- 📂 Organizes projects into PARA buckets (Projects, Areas, Resources, Archives)
- ✅ Enriches tasks with GTD metadata (next actions, contexts, energy level, etc.)
- 📊 Outputs a structured JSON document for further processing

## Installation

This module is part of the monorepo and is built with Bazel:

```bash
# Build the module
bazel build //python/todost

# Run the module
bazel run //python/todost:todost -- --token=<YOUR_TODOIST_API_TOKEN>
```

## Usage

### CLI

```bash
# Run with Bazel
bazel run //python/todost:todost -- --token=<YOUR_TODOIST_API_TOKEN> --outfile=my_export.json

# Or directly if using a virtual environment
python -m python.todost.todost --token=<YOUR_TODOIST_API_TOKEN>
```

### Programmatic Usage

```python
import asyncio
from python.todost.todost import export

async def main():
    await export(
        token="your_todoist_api_token",
        outfile="my_export.json",
        rules_path="path/to/custom_rules.yaml"  # Optional
    )

if __name__ == "__main__":
    asyncio.run(main())
```

## Configuration

The module uses a YAML configuration file to define rule patterns for task categorization and enrichment. The default configuration is in `para_rules.yaml`.

### Rule Types

1. **Regex Rules** - Match patterns in task content/description:
   ```yaml
   regex_rules:
     - pattern: "@([a-z0-9]+)"
       field: "context"
       value: ["$1"]  # Captures contexts like @home, @phone
   ```

2. **Label Rules** - Apply special meaning to Todoist labels:
   ```yaml
   label_rules:
     "next":
       field: "next_action"
       value: true
   ```

3. **Bucket Overrides** - Force projects into specific PARA buckets:
   ```yaml
   bucket_overrides:
     2342342342: "projects"  # Project ID: PARA bucket
   ```

## Development

### Testing

```bash
# Unit tests
python -m pytest python/todost/test_todost.py

# Integration tests (requires valid Todoist API token)
TODOIST_API_TOKEN=your_token python -m pytest python/todost/integration_test_todost.py -v
```

### Linting

```bash
ruff check python/todost/
```

## Output Format

The exported JSON follows this structure:

```json
{
  "meta": {
    "exported": "2025-04-23T14:30:00+00:00",
    "version": 1
  },
  "projects": [...],
  "areas": [...],
  "resources": [...],
  "archives": {
    "completed_tasks": []
  }
}
```

Each project contains sections and tasks, with tasks enriched with GTD metadata like context, energy level, and next action status.

## Dependencies

- `httpx` - Async HTTP client for API requests
- `pydantic` - Data validation and serialization
- `pyyaml` - YAML parsing for rules configuration
- `typer` - CLI interface