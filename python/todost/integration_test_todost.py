"""Integration tests for the Todoist→PARA+GTD exporter.

These tests require a valid Todoist API token in the TODOIST_API_TOKEN 
environment variable. They're designed to run against the actual API
and verify end-to-end functionality.

To run:
    TODOIST_API_TOKEN="your_token" pytest -v python/todost/integration_test_todost.py
    
Or with Bazel:
    TODOIST_API_TOKEN="your_token" bazel test --test_tag_filters=integ //python/todost:integration_test
"""

import os
import pytest
import tempfile
from pathlib import Path

from python.todost.todost import export


@pytest.mark.integ
def test_export_integration():
    """Basic integration test for export functionality.
    
    This test is tagged with 'integ' and will only run when specifically requested.
    """
    # Skip if no token is available
    if "TODOIST_API_TOKEN" not in os.environ:
        pytest.skip("TODOIST_API_TOKEN environment variable not set")
    
    # Use a temporary file for the output
    with tempfile.NamedTemporaryFile(suffix=".json") as temp:
        # Run the export
        export(
            token=os.environ["TODOIST_API_TOKEN"],
            outfile=temp.name,
            rules_path=Path("python/todost/para_rules.yaml")
        )
        
        # Verify the file was created and contains data
        assert os.path.exists(temp.name)
        assert os.path.getsize(temp.name) > 0