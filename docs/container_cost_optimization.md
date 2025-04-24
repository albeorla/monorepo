# Container Registry Cost Optimization

This document outlines strategies for monitoring and optimizing container registry costs in the monorepo.

## Cost Structure

GitHub Container Registry (GHCR) costs are based on:

1. **Storage**: The size and number of container images stored
2. **Data Transfer**: Egress bandwidth when pulling images
3. **Actions Minutes**: Time spent in GitHub Actions building images

## Monitoring Strategy

### Storage Monitoring

Our approach to monitoring storage costs:

1. **Size tracking**: We track image size trends over time
2. **Layer analysis**: We analyze layer composition to identify optimization opportunities
3. **Repository monitoring**: We track the total number and size of repositories

### Bandwidth Monitoring

For monitoring data transfer costs:

1. **Pull metrics**: We monitor the number and geographic distribution of pulls
2. **Caching effectiveness**: We monitor cache hit rates and pull performance

### Actions Monitoring

For CI/CD costs:

1. **Build times**: We track the time spent building images in GitHub Actions
2. **Cache efficiency**: We monitor cache hit rates for build steps

## Cost Optimization Techniques

### Image Size Optimization

We implement these strategies to minimize image size:

1. **Distroless base images**: Using minimal base images without package managers or shells
2. **Layer optimization**:
   - Combining related operations in single layers
   - Ordering operations to maximize layer reuse
   - Cleaning up temporary files within the same layer
3. **Multi-stage builds**: Using build stages to exclude build tools from the final image
4. **Dependency management**: Including only necessary dependencies

### Lifecycle Management

To minimize storage costs:

1. **Automatic cleanup**: Untagged images older than 30 days are deleted
2. **Tag retention**: Only keep important tags (latest, semantic versions)
3. **Layer deduplication**: Reuse layers across images where possible

### CI Optimization

To minimize CI costs:

1. **Bazel caching**: Using Bazel's remote caching to speed up builds
2. **GitHub Actions caching**: Caching dependencies between workflow runs
3. **Conditional builds**: Only rebuilding images when their dependencies change

## Implementation

### Retention Policies

GHCR retention policies are configured to:

1. Delete untagged images after 30 days
2. Keep all tagged images indefinitely

### Monitoring Reports

We generate cost monitoring reports:

1. **Monthly summary**: Total storage, average size, month-over-month growth
2. **Per-service breakdown**: Size and pull counts per service
3. **Optimization opportunities**: Identified large layers or inefficient patterns

### Alerting

Cost alerts are configured for:

1. **Storage threshold**: Alert when total storage exceeds predefined limit
2. **Growth rate**: Alert when month-over-month growth exceeds threshold
3. **Large images**: Alert when individual images exceed size threshold
4. **CI time**: Alert when CI build time for images exceeds threshold

## Best Practices for Developers

When creating or modifying container images:

1. **Include only necessary files** in the image context
2. **Minimize the number of layers** by combining related operations
3. **Clean up temporary files** in the same layer they were created
4. **Use .dockerignore** to exclude unnecessary files
5. **Audit dependencies** regularly to remove unused ones
6. **Test image size impact** before committing changes
7. **Use the standard base images** provided by the monorepo