"""Registry configuration for container images.

This module provides configuration and utilities for publishing container images
to GitHub Container Registry (GHCR). It standardizes repository naming,
versioning, and metadata across the monorepo.

Examples:
    load("//tools/oci:registry.bzl", "ghcr_push")

    # Push an image to GHCR
    ghcr_push(
        name = "push_to_ghcr",
        image = ":my_image",
        repository = "my_service",
        tags = ["latest", "v1.0.0"],
    )
"""

load("@rules_oci//oci:defs.bzl", "oci_push")

# Organization name for GitHub Container Registry
_GHCR_ORG = "albeorla"

# Standard OCI labels
_STANDARD_LABELS = {
    "org.opencontainers.image.source": "https://github.com/albeorla/monorepo",
    "org.opencontainers.image.vendor": "Monorepo Team",
    "org.opencontainers.image.licenses": "MIT",
}

def _get_full_repository_name(repository):
    """Constructs a full GHCR repository name.
    
    Args:
        repository: Base repository name (usually the service name)
        
    Returns:
        Full GHCR repository name 
    """
    return "ghcr.io/{}/{}".format(_GHCR_ORG, repository)

def _get_default_tags():
    """Returns default tags for images.
    
    In a real CI environment, this would dynamically generate tags based on 
    git context (branch, commit hash, tags, etc.), but for development purposes
    we use a simple static tag.
    
    Returns:
        List of default tags
    """
    return ["latest", "dev"]

def _add_standard_labels(labels = None):
    """Adds standard labels to the provided labels.
    
    Args:
        labels: Optional dictionary of labels to extend
        
    Returns:
        Dictionary with standard labels added
    """
    result = dict(_STANDARD_LABELS)
    if labels:
        result.update(labels)
    return result

def ghcr_push(
        name,
        image,
        repository,
        tags = None,
        labels = None,
        **kwargs):
    """Pushes an image to GitHub Container Registry (GHCR).
    
    This macro creates an oci_push target that pushes the specified image to
    GHCR with standard configuration.
    
    Args:
        name: Name of the oci_push target
        image: Label of the image to push
        repository: Base repository name (usually the service name)
        tags: Optional list of tags to apply (defaults to ["latest", "dev"])
        labels: Optional dictionary of labels to apply to the image
        **kwargs: Additional arguments to pass to oci_push
    """
    full_repository = _get_full_repository_name(repository)
    
    # Use provided tags or default tags
    image_tags = tags if tags else _get_default_tags()
    
    # Add standard labels
    image_labels = _add_standard_labels(labels)
    
    # Create the oci_push target
    oci_push(
        name = name,
        image = image,
        repository = full_repository,
        tags = image_tags,
        **kwargs
    )

def ghcr_development_push(
        name,
        image,
        repository,
        **kwargs):
    """Creates a development push target for local testing.
    
    This is a simplified version of ghcr_push that only pushes the latest tag
    and is intended for local development and testing.
    
    Args:
        name: Name of the oci_push target
        image: Label of the image to push
        repository: Base repository name (usually the service name)
        **kwargs: Additional arguments to pass to oci_push
    """
    ghcr_push(
        name = name,
        image = image,
        repository = repository,
        tags = ["dev", "latest"],
        **kwargs
    )

def get_repository_name(service_name):
    """Gets the full repository name for a service.
    
    This is useful for documenting the repository name in other contexts.
    
    Args:
        service_name: Name of the service
        
    Returns:
        Full GHCR repository name
    """
    return _get_full_repository_name(service_name)