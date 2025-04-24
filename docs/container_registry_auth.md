# Container Registry Authentication

This document describes how to set up authentication for the GitHub Container Registry (GHCR) used by this monorepo.

## Overview

We use GitHub Container Registry (GHCR) to store and distribute container images. Authentication is required for:

1. Pushing images (always)
2. Pulling private images (if you decide to make them private)

## Local Development Authentication

To authenticate with GHCR for local development:

1. Create a GitHub Personal Access Token (PAT) with the appropriate permissions:
   - Go to [GitHub Settings > Developer settings > Personal access tokens](https://github.com/settings/tokens)
   - Create a new token with the `write:packages` and `read:packages` scopes

2. Log in to GHCR using Docker CLI:
   ```bash
   export GITHUB_USERNAME=your-github-username
   export GITHUB_TOKEN=your-personal-access-token
   
   echo $GITHUB_TOKEN | docker login ghcr.io -u $GITHUB_USERNAME --password-stdin
   ```

3. (Optional) Store the credentials in a secure location for reuse:
   ```bash
   # Save to keychain, credential manager, or similar
   # This is platform-specific, see Docker documentation
   ```

Once authenticated, you can use the push targets defined in the BUILD files:
```bash
bazel run //python/hello_python:hello_python_image_push
```

## CI/CD Authentication

For GitHub Actions workflows, authentication to GHCR is handled automatically using the built-in `GITHUB_TOKEN`. The workflow is configured in `.github/workflows/container-publish.yml` and includes:

```yaml
- name: Login to GitHub Container Registry
  uses: docker/login-action@v3
  with:
    registry: ghcr.io
    username: ${{ github.actor }}
    password: ${{ secrets.GITHUB_TOKEN }}
```

This token has the necessary permissions to push to GHCR within the repository's scope.

## Repository Permissions

By default, container images in GHCR inherit permissions from their linked GitHub repository. If you need to adjust access:

1. Go to your package on the GitHub UI (e.g., `https://github.com/users/albeorla/packages/container/package/hello_python`)
2. Click on "Package settings"
3. Configure access settings as needed

For organization repositories, you can also set organization-wide policies.

## Troubleshooting

### Authentication Failures

If you encounter authentication issues:

1. **Check token scopes**: Ensure your PAT has the `write:packages` scope
2. **Check token expiration**: PATs can expire, create a new one if needed
3. **Check Docker credentials store**: Remove old credentials with `docker logout ghcr.io`
4. **Check repository permissions**: Ensure you have write access to the repository

### Push Failures

If authentication succeeds but pushes fail:

1. **Check repository name**: Ensure the repository name matches the GitHub username/organization
2. **Check formatting**: The repository format should be `ghcr.io/username/repository`
3. **Check image tag**: Ensure the tag follows the allowed format

## Best Practices

1. **Use short-lived tokens**: Regularly rotate PATs for development
2. **Never commit tokens**: Keep tokens out of version control
3. **Use OIDC when possible**: For production deployments, consider OIDC authentication
4. **Use CI for production publishing**: Let GitHub Actions handle production pushes