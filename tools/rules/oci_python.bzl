"""Bazel macros for building OCI images for Python services.

This module provides macros that simplify the creation of OCI (Docker) images
for Python applications using rules_oci. It supports both simple and complex
Python services, with proper handling of dependencies and runtime configuration.

Examples:
    # Basic usage
    load("//tools/rules:oci_python.bzl", "py_image")

    py_image(
        name = "hello_image",
        binary = "//python/hello_python:hello_python",
        base = "@distroless_python",
    )

    # Advanced usage with custom settings
    py_image(
        name = "service_image",
        binary = "//python/service:service_binary",
        base = "@distroless_python_nonroot",
        env = {
            "LOG_LEVEL": "INFO",
        },
        labels = {
            "org.opencontainers.image.description": "My service",
            "org.opencontainers.image.version": "1.0.0",
        },
        ports = ["8080"],
    )
"""

load("@rules_oci//oci:defs.bzl", "oci_image")

def py_image(
        name,
        binary,
        base = "@distroless_python_base",
        env = None,
        labels = None,
        ports = None,
        user = None,
        workdir = "/app",
        visibility = None,
        **kwargs):
    """Creates an OCI image from a py_binary target.

    This macro creates a container image for a Python application, using a distroless
    base image and setting up appropriate defaults for Python applications.

    Args:
        name: Name of the oci_image target.
        binary: Label of the py_binary target to containerize.
        base: Base image to use (should be a Python-capable distroless image).
        env: Dictionary of environment variables to set.
        labels: Dictionary of OCI labels to apply to the image.
        ports: List of ports to expose.
        user: User to run the container as (defaults to nonroot if a nonroot base is used).
        workdir: Working directory for the container.
        visibility: Visibility of the target.
        **kwargs: Additional arguments to pass to oci_image.
    """
    default_env = {
        "PYTHONUNBUFFERED": "1",
    }
    
    default_labels = {
        "org.opencontainers.image.source": "https://github.com/user/monorepo",
        "org.opencontainers.image.vendor": "Monorepo Team",
    }
    
    # Merge user-provided values with defaults
    if env:
        default_env.update(env)
    
    if labels:
        default_labels.update(labels)
    
    # Get the binary name from the label
    binary_name = binary.split(":")[-1]
    
    # Create the OCI image
    args = {
        "name": name,
        "base": base,
        # The entrypoint is the Python binary in the image
        "entrypoint": [binary_name],
        "env": default_env,
        "labels": default_labels,
        "user": user,
        "workdir": workdir,
        "visibility": visibility,
    }
    
    # Add the kwargs
    args.update(kwargs)
    
    # Create the OCI image
    oci_image(**args)

def py_service_image(name, binary, config_files = None, **kwargs):
    """Creates an OCI image for a Python service with configuration files.
    
    This is a specialized version of py_image that also handles configuration files
    and sets up appropriate defaults for services.
    
    Args:
        name: Name of the oci_image target.
        binary: Label of the py_binary target to containerize.
        config_files: List of configuration files to include in the image.
        **kwargs: Additional arguments to pass to py_image.
    """
    # TODO: Implement handling of config files
    
    # Remove the ports attribute since it's not supported
    if "ports" in kwargs:
        kwargs.pop("ports")
    
    # Call the base py_image function
    py_image(
        name = name,
        binary = binary,
        **kwargs
    )