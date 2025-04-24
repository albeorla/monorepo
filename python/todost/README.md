# Todoist → PARA+GTD Exporter

A Python module for exporting [Todoist](https://todoist.com/) tasks, projects, and sections to a structured JSON format following the PARA (Projects, Areas, Resources, Archives) method and GTD (Getting Things Done) principles.

## Features

- 🔄 Fetches data from Todoist REST API v2
- 🧠 Applies rule-based categorization using regex patterns and labels
- 📂 Organizes projects into PARA buckets (Projects, Areas, Resources, Archives)
- ✅ Enriches tasks with GTD metadata (next actions, contexts, energy level, etc.)
- 📊 Outputs a structured JSON document for further processing
- 🐳 Supports containerized execution via Docker

## Quick Start

The easiest way to run todost is using the provided helper script:

```bash
# 1. Copy the example environment file and edit it with your Todoist API token
cp .env.example .env
# Edit .env to add your actual Todoist API token

# 2. Run the helper script
./run_todost.sh
```

This will create a `todoist_gtd_para.json` file with your exported data.

## Configuration

### API Token

You need a Todoist API token to use this tool. You can get one from the [Todoist Integrations settings page](https://todoist.com/app/settings/integrations).

Set up your token using one of these methods:

1. **Environment File** (recommended):
   - Copy `.env.example` to `.env`
   - Add your token to the `.env` file
   - Run using `./run_todost.sh`

2. **Direct Environment Variable**:
   ```bash
   export TODOIST_API_TOKEN=your_token_here
   ./run_todost.sh
   ```

3. **Command Line Argument**:
   ```bash
   # With Bazel
   bazel run //python/todost:todost -- "your_token_here"
   
   # With Python
   python todost.py "your_token_here"
   ```

### Output File

By default, output is saved to `todoist_gtd_para.json`. Customize using:

1. **Environment Variable**:
   ```bash
   export TODOST_OUTPUT_FILE=custom_name.json
   ./run_todost.sh
   ```

2. **Command Line Argument**:
   ```bash
   # With Bazel
   bazel run //python/todost:todost -- --outfile=custom_name.json "your_token_here"
   
   # With Python
   python todost.py --outfile=custom_name.json "your_token_here"
   ```

## Running todost

### Using the Helper Script (Recommended)

```bash
# Set up environment first
cp .env.example .env  # Then edit .env to add your token

# Run the exporter with Python
./run_todost.sh

# Run with Docker container
./run_todost.sh --container
```

### Using Bazel

```bash
# Make sure you're in the repository root
bazel run //python/todost:todost -- --outfile=my_export.json "your_token_here"
```

### Using Python Directly

```bash
# Create and activate a virtual environment
cd /path/to/monorepo
./scripts/setup_venv.sh
source .venv/bin/activate

# Run the tool
cd python/todost
python todost.py --outfile=my_export.json "your_token_here"
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

## Container Usage

You can also run todost as a container for improved isolation and deployment flexibility.

### Building the Container

```bash
# Build the container image
bazel build //python/todost:todost_image

# Push to GitHub Container Registry (requires authentication)
bazel run //python/todost:ghcr_development_push
```

### Running with Docker

```bash
# Pull the image (if not building locally)
docker pull ghcr.io/albeorla/todost:latest

# Run with environment variables
docker run -e TODOIST_API_TOKEN=your_token_here \
           -e TODOST_OUTPUT_FILE=/data/output.json \
           -v $(pwd):/data \
           ghcr.io/albeorla/todost:latest
```

### Configuration

When running as a container, you can:

1. **Pass Environment Variables**: Use Docker's `-e` flag to set environment variables:
   - `TODOIST_API_TOKEN`: Your Todoist API token
   - `TODOST_OUTPUT_FILE`: Output file path (inside container)
   - `LOG_LEVEL`: Set to DEBUG for verbose output

2. **Mount Volumes**: Use Docker's `-v` flag to mount volumes:
   - Mount a directory to store the output file
   - Mount a custom rules file with `-v path/to/rules.yaml:/app/para_rules.yaml`

## PARA + GTD Rules Configuration

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

## Testing

```bash
# Unit tests
python -m pytest python/todost/test_todost.py

# Integration tests (requires valid Todoist API token)
TODOIST_API_TOKEN=your_token python -m pytest python/todost/integration_test_todost.py -v

# With Bazel
bazel test //python/todost:todost_test
TODOIST_API_TOKEN=your_token bazel test //python/todost:integration_test
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

## Troubleshooting

### Common Issues

1. **API Token Invalid**
   - Make sure your Todoist API token is correct
   - Check that it hasn't expired or been revoked

2. **Missing Dependencies**
   - Ensure you're using the environment set up by `setup_venv.sh`
   - Or install dependencies: `pip install httpx pydantic pyyaml typer`

3. **Network Issues**
   - Check your internet connection
   - Verify that you can access the Todoist API from your network

4. **Container Issues**
   - Ensure Docker is installed and running
   - Check that you have permissions to run Docker commands
   - For custom configurations, verify volume mounts and environment variables

### Debug Mode

For more verbose output, set the `LOG_LEVEL` environment variable:

```bash
export LOG_LEVEL=DEBUG
./run_todost.sh
```

## Dependencies

- `httpx` - Async HTTP client for API requests
- `pydantic` - Data validation and serialization
- `pyyaml` - YAML parsing for rules configuration
- `typer` - CLI interface