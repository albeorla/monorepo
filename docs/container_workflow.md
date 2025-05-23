# Container Workflow

This document describes the container infrastructure in the monorepo, including how to build, test, and deploy containerized applications.

## Overview

The monorepo uses [Bazel](https://bazel.build) with [rules_oci](https://github.com/bazel-contrib/rules_oci) to build [OCI](https://opencontainers.org/) (Docker) images for services. This provides:

- Reproducible builds with exact dependency pinning
- Secure distroless base images that minimize attack surface
- Efficient incremental rebuilds through Bazel's caching
- Standardized container configuration across services
- Automated publishing to GitHub Container Registry

## Base Images

We use Google's distroless Python images for security and performance benefits. These images:

- Contain only Python runtime and necessary libraries, not shell or package managers
- Are significantly smaller than traditional images
- Reduce attack surface by removing unnecessary components
- Support Python 3.11, which is our standard runtime version

Available variants:

- `@distroless_python_base` - Standard Python 3.11 runtime 
- `@distroless_python_nonroot` - Python 3.11 runtime that runs as non-root user (recommended for most services)
- `@distroless_python_debug` - Includes busybox shell for debugging (use only for troubleshooting)

## Building Container Images

### Simple Service

For a simple Python service, add these targets to your `BUILD.bazel` file:

```python
load("//tools/rules:oci_python.bzl", "py_image")
load("@rules_oci//oci:defs.bzl", "oci_push")

# First define your py_binary target as usual
py_binary(
    name = "my_service",
    srcs = ["main.py"],
    deps = [":my_service_lib"],
)

# Then add container image configuration
py_image(
    name = "my_service_image",
    binary = ":my_service",
    base = "@distroless_python_nonroot",  # Recommended base image
    env = {
        # Add environment variables if needed
        "LOG_LEVEL": "INFO",
    },
    labels = {
        "org.opencontainers.image.description": "My service description",
        "org.opencontainers.image.version": "1.0.0",
    },
)

# Add a target to load the image into Docker
oci_push(
    name = "my_service_image_load",
    image = ":my_service_image",
    repository = "localhost/my_service",
    format = "docker",
)
```

### Building and Running

```bash
# Build the container image
bazel build //path/to/service:my_service_image

# Load the image into Docker
bazel run //path/to/service:my_service_image_load

# Run the container
docker run -it --rm localhost/my_service
```

## Configuration for Different Service Types

### Services with Configuration Files

For services that require configuration files, ensure the files are included in the `data` attribute of your `py_binary` target:

```python
py_binary(
    name = "config_service",
    srcs = ["main.py"],
    deps = [":config_service_lib"],
    data = ["config.yaml"],  # Include config files
)
```

### Services with External Dependencies

External Python dependencies from PyPI are automatically included in the container image. Make sure they are properly declared in your `py_library` target's `deps` attribute:

```python
py_library(
    name = "service_lib",
    srcs = ["service.py"],
    deps = [
        "@pip//requests:pkg",
        "@pip//pydantic:pkg",
        # Other dependencies
    ],
)
```

## Custom Image Macros

The monorepo provides custom macros to simplify container creation:

- `py_image`: Basic container image for Python applications
- `py_service_image`: Enhanced configuration for services with config files

These macros set sensible defaults for most services while allowing customization when needed.

## Security Considerations

1. **Always use nonroot base images** for production services (`@distroless_python_nonroot`)
2. **Never store secrets in container images** - use environment variables or mounted secrets instead
3. **Keep dependencies updated** to avoid security vulnerabilities
4. **Minimize image size** by only including necessary files and dependencies

## Continuous Integration

CI automatically builds container images for all services on:
- Merges to the main branch
- Release tags

The workflow:
1. Builds the container image with Bazel
2. Tags images based on git context (commit hash, branch, tag)
3. Runs security scanning with Trivy
4. Pushes images to the registry (if on main branch or tag)

## Cost Optimization

To minimize container storage and bandwidth costs:

1. Use distroless base images to keep image sizes small
2. Leverage Bazel's layering to optimize caching
3. Use CI to automatically clean up old untagged images
4. Monitor image size trends in the FinOps dashboard

## Troubleshooting

### Common Issues

1. **Image build fails with dependency errors**
   - Check that all dependencies are properly declared in `deps`
   - Verify that `requirements_lock.txt` has the correct versions

2. **Container runs but can't find files**
   - Ensure files are included in the `data` attribute of the `py_binary`
   - Check file paths in your code (use relative paths to the running directory)

3. **Permission denied errors**
   - Distroless nonroot images run as user 65532 with limited permissions
   - Ensure your application doesn't need to write to protected directories

### Debugging with shell access

If you need to debug issues inside the container:
```bash
# Build using the debug variant
py_image(
    name = "debug_image",
    binary = ":my_service",
    base = "@distroless_python_debug",  # Includes busybox shell
)

# Run with shell
docker run -it --rm localhost/my_service sh
```

## Container Registry

We use GitHub Container Registry (GHCR) to store and distribute container images. Benefits include:

- Native integration with GitHub Actions
- Free for public repositories
- Fine-grained access control
- Vulnerability scanning
- Automatic build and push from GitHub Actions

### Registry Structure

- All images are published to `ghcr.io/albeorla/{service_name}`
- Standard tags include:
  - `latest`: Most recent main branch build
  - Semantic versions: e.g., `1.0.0` for tagged releases
  - PR numbers: e.g., `pr-123` for pull request builds (optional)

### Services with Container Support

The following services currently have container support:

- **hello_python**: Basic Python demo service
- **todost**: Todoist → PARA+GTD exporter utility
  - Supports running with Docker directly via `./run_todost.sh --container`
  - Available at `ghcr.io/albeorla/todost`
  - Tags: `latest`, `v1.0.0`

### Publishing Images

#### Local Development

For local development and testing, use:

```bash
# Login to GHCR (needed once)
echo $GITHUB_TOKEN | docker login ghcr.io -u $GITHUB_USERNAME --password-stdin

# Build and push with development tag
bazel run //python/hello_python:ghcr_development_push

# For todost
bazel run //python/todost:ghcr_development_push
```

#### CI/CD Publishing

GitHub Actions automatically builds and publishes images on:
- Pushes to main branch (tagged as `latest`)
- Release tags (tagged as both `latest` and the version number)

The workflow is defined in `.github/workflows/container-publish.yml`.

### Security Scanning

Container images are automatically scanned for vulnerabilities using Trivy. The scan checks for:
- OS vulnerabilities
- Language-specific package vulnerabilities
- Security issues in application dependencies

Critical or high severity issues will cause the CI build to fail.

### Cost Optimization

To minimize storage costs and improve security:
- Old untagged images are automatically cleaned up
- Images are built with minimal layers for efficient storage
- Only necessary files are included in the container

## Next Steps

- Implement image promotion workflow for staging/production
- Create integration tests for containerized services
- Set up multi-architecture builds (amd64, arm64)