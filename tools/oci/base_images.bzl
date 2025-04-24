"""Base image configuration for OCI images.

This file defines the base images used for building container images in the monorepo.
It focuses on distroless images for security and size optimization.
"""

load("@rules_oci//oci:pull.bzl", "oci_pull")

def register_base_images():
    """Registers all base images used in the monorepo."""
    
    # Python base images
    
    # Standard Python 3.11 distroless image (Debian 12 based)
    oci_pull(
        name = "distroless_python_base",
        digest = "sha256:3bedc7d1518d866c166b1b734ed8220a3b56c7784fed61ac89acce04736a6a7e",
        image = "gcr.io/distroless/python3-debian12",
        platforms = [
            "linux/amd64",
            "linux/arm64/v8",
        ],
    )
    
    # Non-root Python 3.11 distroless image for enhanced security
    oci_pull(
        name = "distroless_python_nonroot",
        digest = "sha256:fd8b24e41a293574a7cbd0847c54d3e58954e3d661a2d15ea5e56c7c0afb5556",
        image = "gcr.io/distroless/python3-debian12:nonroot",
        platforms = [
            "linux/amd64",
            "linux/arm64/v8",
        ],
    )
    
    # Debug variant with shell for troubleshooting
    oci_pull(
        name = "distroless_python_debug",
        digest = "sha256:7a0e0acd85978302a5e3112e0f9bb82e5bf2c456178f5ac6202bd30e0f1b4345",
        image = "gcr.io/distroless/python3-debian12:debug",
        platforms = [
            "linux/amd64",
            "linux/arm64/v8",
        ],
    )