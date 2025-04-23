# Testing GitHub Actions Workflows

This document provides guidance on how to validate and test the GitHub Actions workflows in this repository before they run in production.

## Prerequisites

- [Act](https://github.com/nektos/act) - A tool for running GitHub Actions locally
- Docker installed and running
- GitHub Personal Access Token (for workflows that interact with GitHub API)

## Installation

1. Install Act:
   ```bash
   # macOS
   brew install act
   
   # Linux
   curl -s https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash
   ```

2. Verify installation:
   ```bash
   act --version
   ```

## Testing Workflows Locally

### Basic Workflow Testing

Test the Python CI workflow:

```bash
# Run the entire workflow
act push -W .github/workflows/python-ci.yml

# Run a specific job
act push -W .github/workflows/python-ci.yml -j python-lint
```

### Setting Up Secrets

For workflows that require secrets:

```bash
# Create a .secrets file (add to .gitignore)
echo "CI_COST_BUDGET=0.10" > .secrets

# Run with secrets
act push -W .github/workflows/python-ci.yml --secret-file .secrets
```

## Validating Workflow Syntax

Use GitHub's workflow syntax checker to validate workflows:

```bash
npx @aorlando/validate-github-workflow .github/workflows/python-ci.yml
```

## Common Issues and Solutions

### Missing Dependencies

Ensure all required dependencies are installed in the workflow:
- Python libraries in the `python-lint` job
- Build dependencies in the `python-build-test` job

### Cost Calculation Issues

The cost calculation uses `awk` for floating-point comparisons. Verify it works correctly with:

```bash
act push -W .github/workflows/python-ci.yml -j check-ci-cost
```

### Security Scan Failures

Trivy security scanning can fail due to vulnerabilities in dependencies. For initial testing, we set:
- `exit-code: '0'` to prevent failing the build
- Once dependencies are clean, change to `exit-code: '1'`

## Production Verification

After pushing changes to GitHub:

1. Check the "Actions" tab in the repository
2. Verify all jobs complete successfully
3. Check the workflow summary for cost reports
4. Review security scan results

## Future Improvements

- Add detailed test coverage reporting
- Implement workflow testing in the CI process itself
- Add performance benchmarking for build/test steps
- Integrate with cost monitoring systems