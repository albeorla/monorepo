"""Integration tests for the Todoist→PARA+GTD exporter."""

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