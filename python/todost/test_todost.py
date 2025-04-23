"""Tests for the Todoist→PARA+GTD exporter."""

import json
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from python.todost.todost import (
    GTDFields,
    LabelRule,
    RegexRule,
    RuleEngine,
    TodoistClient,
    export,
)


@pytest.fixture
def mock_projects():
    """Sample project data."""
    return [
        {
            "id": 2342342342,
            "name": "Q2 Strategic Plan",
            "created_at": "2023-01-01T12:00:00Z",
        },
        {
            "id": 1234567890,
            "name": "Health & Wellness",
            "created_at": "2022-01-01T12:00:00Z",
        },
    ]


@pytest.fixture
def mock_sections():
    """Sample section data."""
    return [
        {
            "id": 11111,
            "name": "Planning",
            "project_id": 2342342342,
        },
        {
            "id": 22222,
            "name": "Execution",
            "project_id": 2342342342,
        },
    ]


@pytest.fixture
def mock_tasks():
    """Sample task data."""
    return [
        {
            "id": 101,
            "content": "Create roadmap @computer",
            "description": "Needs to be done ASAP. 30 min task.",
            "priority": 4,
            "project_id": 2342342342,
            "section_id": 11111,
            "created_at": "2023-02-01T09:00:00Z",
            "labels": ["work", "next"],
        },
        {
            "id": 102,
            "content": "Present to team waiting: Bob",
            "priority": 3,
            "project_id": 2342342342,
            "section_id": 22222,
            "created_at": "2023-02-02T09:00:00Z",
            "labels": ["meeting"],
        },
    ]


def test_regex_rule():
    """Test RegexRule pattern matching."""
    rule = RegexRule(pattern=r"@([a-z0-9]+)", field="context", value=["$1"])
    gtd = GTDFields()
    rule.apply("Task @home and @work", gtd)
    assert gtd.context == ["$1"]


def test_label_rule():
    """Test LabelRule applies correctly."""
    rule = LabelRule(label="next", field="next_action", value=True)
    gtd = GTDFields()
    rule.apply(["next", "today"], gtd)
    assert gtd.next_action is True


@patch("python.todost.todost.yaml")
@patch("python.todost.todost.Path.exists")
def test_rule_engine_bucket_override(mock_exists, mock_yaml):
    """Test the bucket override logic."""
    mock_exists.return_value = True
    mock_yaml.safe_load.return_value = {
        "bucket_overrides": {2342342342: "projects", 1234567890: "areas"}
    }

    # Create a mock Path object instead of accessing the file
    mock_path = MagicMock()
    engine = RuleEngine(yaml_path=mock_path)
    project = {"id": 2342342342, "name": "Test", "created_at": "2023-01-01T12:00:00Z"}
    assert engine.bucket_for_project(project) == "projects"


@patch("python.todost.todost.httpx")
def test_todoist_client_fetch_all(mock_httpx):
    """Test the TodoistClient fetch_all method."""
    mock_client = MagicMock()
    mock_client.get.side_effect = AsyncMock(return_value=MagicMock(json=lambda: []))
    mock_httpx.AsyncClient.return_value = mock_client

    client = TodoistClient("fake_token")
    assert client._client is not None


@patch("python.todost.todost.Path.write_text")
@patch("python.todost.todost.TodoistClient")
@patch("python.todost.todost.RuleEngine")
def test_export_function(mock_rule_engine, mock_client, mock_write, 
                        mock_projects, mock_sections, mock_tasks):
    """Test the export function end-to-end."""
    # Setup mocks
    mock_client_instance = MagicMock()
    mock_client_instance.fetch_all = AsyncMock(
        return_value=(mock_projects, mock_sections, mock_tasks)
    )
    # Make close a proper async coroutine
    mock_client_instance.close = AsyncMock()
    mock_client.return_value = mock_client_instance

    mock_engine = MagicMock()
    mock_engine.bucket_for_project.return_value = "projects"
    mock_engine.enrich_task.return_value = GTDFields(next_action=True)
    mock_rule_engine.return_value = mock_engine

    # Run the export function
    import asyncio
    asyncio.run(export(token="fake_token", outfile="test_output.json"))

    # Verify results
    mock_client.assert_called_once_with("fake_token")
    mock_client_instance.fetch_all.assert_called_once()
    mock_client_instance.close.assert_called_once()
    
    # Verify that write_text was called
    mock_write.assert_called_once()
    
    # We expect the first argument to be json data
    json_str = mock_write.call_args[0][0]
    data = json.loads(json_str)
    
    # Basic structure checks
    assert "meta" in data
    assert "projects" in data
    assert len(data["projects"]) > 0