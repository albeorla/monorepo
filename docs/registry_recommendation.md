# Container Registry Recommendation

## Executive Summary

This document evaluates container registry options for the monorepo's container infrastructure. Based on our analysis, we recommend **GitHub Container Registry (GHCR)** as the primary registry due to its free tier for our use case, tight integration with our GitHub-based workflow, and native GitHub Actions support.

## Requirements

Our container registry solution must satisfy these requirements:

1. **Bazel Integration**: Compatible with rules_oci for building and publishing
2. **CI Automation**: Seamless integration with GitHub Actions
3. **Cost Efficiency**: Minimal cost for our expected usage patterns
4. **Security**: Support for vulnerability scanning and access control
5. **Developer Experience**: Easy to use for developers
6. **Performance**: Reliable and fast globally

## Options Analysis

### GitHub Container Registry (GHCR)

| Category | Assessment |
|----------|------------|
| **Cost** | Free for public repositories, included with GitHub plans for private repositories |
| **Bazel Compatibility** | ✅ Full compatibility with rules_oci via `ghcr.io/owner/image` format |
| **CI Integration** | ✅ Native GitHub Actions integration with GITHUB_TOKEN |
| **Security** | ✅ Fine-grained access control, repository-level permissions, vulnerability scanning |
| **Features** | Container package management, metadata, versioning |
| **Limitations** | Tied to GitHub ecosystem |

**Pros**:
- Native GitHub Actions integration
- GitHub authentication reuse
- Free for our usage pattern
- Already part of our toolchain
- Fine-grained access controls

**Cons**:
- GitHub ecosystem lock-in
- Less advanced features than cloud provider registries

### Docker Hub

| Category | Assessment |
|----------|------------|
| **Cost** | Free for public repositories, limited free private repositories |
| **Bazel Compatibility** | ✅ Full compatibility with rules_oci |
| **CI Integration** | Requires explicit authentication configuration |
| **Security** | Basic access controls, paid plans for more security features |
| **Features** | Largest public repository ecosystem |
| **Limitations** | Pull rate limits, limited private repositories on free tier |

**Pros**:
- Industry standard
- Wide ecosystem
- Good documentation

**Cons**:
- Pull rate limits on free tier
- Limited private repositories
- Less integrated with GitHub Actions

### AWS Elastic Container Registry (ECR)

| Category | Assessment |
|----------|------------|
| **Cost** | Pay-per-use ($0.10 per GB-month storage, data transfer costs) |
| **Bazel Compatibility** | ✅ Compatible with credential helper configuration |
| **CI Integration** | Requires AWS credential management |
| **Security** | ✅ IAM-based access control, vulnerability scanning, lifecycle policies |
| **Features** | Cross-region replication, image signing |
| **Limitations** | Region-specific repositories, complex IAM setup |

**Pros**:
- Enterprise-grade security
- Advanced features like lifecycle policies
- Integrated with AWS ecosystem

**Cons**:
- Cost for our simple needs
- More complex setup and maintenance
- Region-specific configuration

### Google Container Registry (GCR) / Artifact Registry

| Category | Assessment |
|----------|------------|
| **Cost** | First 0.5GB free, then $0.10 per GB-month, network costs |
| **Bazel Compatibility** | ✅ Fully compatible |
| **CI Integration** | Requires Google Cloud credential management |
| **Security** | ✅ IAM access control, vulnerability scanning |
| **Features** | Integration with Google Cloud Build |
| **Limitations** | Some features only available through Google Cloud console |

**Pros**:
- Good Bazel integration (Google maintains Bazel)
- Reliable performance
- Integrated with GCP ecosystem

**Cons**:
- Cost for our simple needs
- Requires GCP credentials management
- Less integrated with GitHub Actions

## Recommendation

We recommend **GitHub Container Registry (GHCR)** for the following reasons:

1. **Seamless GitHub Actions Integration**: Native support with GITHUB_TOKEN
2. **Cost Efficiency**: Free for our use case with public repositories
3. **Reduced Complexity**: Reuse existing GitHub authentication
4. **Sufficient Security**: Repository-level permissions and vulnerability scanning
5. **Developer Experience**: Integrated with our existing GitHub workflow

This recommendation prioritizes developer experience and CI integration while keeping costs minimal. As the project grows, we can reassess and potentially migrate to a more feature-rich solution like AWS ECR or GCR if needed.

## Implementation Plan

1. Set up GitHub Container Registry for our organization
2. Configure rules_oci to publish to GHCR
3. Set up GitHub Actions workflow for automated publishing
4. Implement vulnerability scanning with GitHub's security features
5. Document the registry workflow for developers

## Future Considerations

- Multi-registry strategy for better availability
- Cloud-specific registries if we adopt specific cloud platforms
- Self-hosted options if we reach volume limitations