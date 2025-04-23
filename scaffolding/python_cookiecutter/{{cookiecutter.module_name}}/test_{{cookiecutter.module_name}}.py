"""Tests for {{cookiecutter.module_name}}."""

import pytest

from python.{{cookiecutter.module_name}}.{{cookiecutter.module_name}} import process_data


def test_process_data():
    """Test the process_data function with sample input."""
    # Arrange
    test_data = {"key": "value", "count": 42}
    
    # Act
    result = process_data(test_data)
    
    # Assert
    assert isinstance(result, list)
    assert len(result) > 0
    assert result[0]["processed"] is True
    assert result[0]["input"] == test_data