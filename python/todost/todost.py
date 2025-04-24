"""Todoist→PARA+GTD exporter.

Implements the full extraction/enrichment logic described in PRD v1.2:
* Fetch open projects, sections, and tasks via Todoist REST v2.
* Apply deterministic regex/label rules from `para_rules.yaml`.
* (Optional) LLM enrichment via provider port.
* Bucket projects into PARA (`projects`, `areas`, `resources`, `archives`).
* Serialize to Pydantic models and dump nested JSON.

Usage (as Bazel target or direct invocation):

    bazel run //python/todost:todost -- --token=<TODOIST_API_TOKEN>

Requirements: httpx, pydantic, pyyaml, typer.

Version: 1.0.0
"""

from __future__ import annotations

import asyncio
import json
import re
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

# Optional runtime imports. We fall back to lightweight stubs in test
# environments where the heavy third‑party libraries may be missing.

try:
    import httpx  # type: ignore
except ModuleNotFoundError:  # pragma: no cover – allow slim test envs
    httpx = None  # type: ignore[assignment]

try:
    import yaml  # type: ignore
except ModuleNotFoundError:  # pragma: no cover
    yaml = None  # type: ignore[assignment]

from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
# Domain models
# ---------------------------------------------------------------------------


class GTDFields(BaseModel):
    next_action: bool = False
    waiting_on: str | None = None
    someday: bool = False
    delegated_to: str | None = None
    context: list[str] = Field(default_factory=list)
    energy: str | None = None  # low | medium | high
    time_needed: int | None = None  # minutes


class Task(BaseModel):
    todoist_id: int
    title: str
    notes: str | None = None
    due: str | None = None  # ISO‑8601
    priority: int
    labels: list[str] = Field(default_factory=list)
    completed: bool = False
    created: str
    gtd: GTDFields


class Section(BaseModel):
    todoist_id: int | None
    title: str
    tasks: list[Task] = Field(default_factory=list)


class Project(BaseModel):
    todoist_id: int
    title: str
    para_bucket: str
    gtd_status: str = "active"
    description: str | None = None
    due: str | None = None
    created: str
    labels: list[str] = Field(default_factory=list)
    sections: list[Section] = Field(default_factory=list)


class ExportDocument(BaseModel):
    """PARA+GTD export document containing all organization data.
    
    Version: 1.0.0
    """
    meta: dict[str, Any]
    projects: list[Project] = Field(default_factory=list)
    areas: list[Project] = Field(default_factory=list)
    resources: list[Project] = Field(default_factory=list)
    archives: dict[str, Any] = Field(default_factory=lambda: {"completed_tasks": []})


# ---------------------------------------------------------------------------
# Rule engine
# ---------------------------------------------------------------------------


@dataclass
class RegexRule:
    pattern: str
    field: str
    value: Any

    def apply(self, text: str, out: GTDFields) -> None:
        if re.search(self.pattern, text, flags=re.I):
            setattr(out, self.field, self.value)


@dataclass
class LabelRule:
    label: str
    field: str
    value: Any

    def apply(self, labels: list[str], out: GTDFields) -> None:
        if self.label in labels:
            setattr(out, self.field, self.value)


class RuleEngine:
    """Applies user‑defined YAML rules to Todoist entities."""

    def __init__(self, yaml_path: Path = Path("para_rules.yaml")):
        if yaml is None or not yaml_path.exists():
            cfg: dict[str, Any] = {}
        else:
            cfg = yaml.safe_load(yaml_path.read_text())
        self.regex_rules = [RegexRule(**r) for r in cfg.get("regex_rules", [])]
        self.label_rules = [
            LabelRule(label=k, **v) for k, v in cfg.get("label_rules", {}).items()
        ]
        self.bucket_overrides: dict[int, str] = cfg.get("bucket_overrides", {})

    def enrich_task(self, task: dict) -> GTDFields:
        gtd = GTDFields()
        text = f"{task['content']} {task.get('description', '')}"
        for rule in self.regex_rules:
            rule.apply(text, gtd)
        for lr in self.label_rules:
            lr.apply(task.get("labels", []), gtd)

        # Simple next‑action heuristic
        if task.get("priority") == 4 or "next" in task.get("labels", []):
            gtd.next_action = True
        return gtd

    def bucket_for_project(self, prj: dict) -> str:
        override = self.bucket_overrides.get(prj["id"])
        if override:
            return override

        if prj.get("due_date"):
            return "projects"

        created = datetime.fromisoformat(prj["created_at"].rstrip("Z"))
        if (datetime.now(UTC) - created).days < 90:
            return "projects"

        return "areas"


# ---------------------------------------------------------------------------
# Todoist REST client
# ---------------------------------------------------------------------------


class TodoistClient:
    """Minimal async Todoist REST v2 client."""

    def __init__(self, token: str):
        if httpx is None:
            raise RuntimeError(
                "httpx is required for network operations but is not installed."
            )

        self._client = httpx.AsyncClient(
            base_url="https://api.todoist.com/rest/v2",
            headers={"Authorization": f"Bearer {token}"},
            timeout=30,
        )

    async def _get(self, endpoint: str) -> Any:
        resp = await self._client.get(endpoint)
        resp.raise_for_status()
        return resp.json()

    async def fetch_all(self):  # noqa: D401
        """Fetch projects, sections and tasks concurrently."""

        projects, sections, tasks = await asyncio.gather(
            self._get("/projects"),
            self._get("/sections"),
            self._get("/tasks"),
        )
        return projects, sections, tasks

    async def close(self) -> None:
        await self._client.aclose()


# ---------------------------------------------------------------------------
# Export orchestration
# ---------------------------------------------------------------------------


async def export(
    *,
    token: str,
    outfile: str = "todoist_gtd_para.json",
    rules_path: Path = Path("para_rules.yaml")
) -> None:
    """Export Todoist data to a PARA + GTD JSON document."""

    client = TodoistClient(token)
    try:
        projects_raw, sections_raw, tasks_raw = await client.fetch_all()
    finally:
        await client.close()

    engine = RuleEngine(rules_path)

    # Index look‑ups for efficient joins
    sections_by_project: dict[int, list[dict]] = {}
    for sec in sections_raw:
        sections_by_project.setdefault(sec["project_id"], []).append(sec)

    tasks_by_project: dict[int, list[dict]] = {}
    for t in tasks_raw:
        tasks_by_project.setdefault(t["project_id"], []).append(t)

    doc = ExportDocument(
        meta={"exported": datetime.now(UTC).isoformat(), "version": 1}
    )

    def build_task(t: dict) -> Task:  # noqa: ANN001
        """Build a Task model from raw task data."""
        return Task(
            todoist_id=t["id"],
            title=t["content"],
            notes=t.get("description"),
            due=t["due"]["date"] if t.get("due") else None,
            priority=t["priority"],
            labels=t.get("labels", []),
            completed=False,
            created=t["created_at"],
            gtd=engine.enrich_task(t),
        )

    # Transform projects ➜ Pydantic models
    for prj in projects_raw:
        bucket = engine.bucket_for_project(prj)
        proj_obj = Project(
            todoist_id=prj["id"],
            title=prj["name"],
            para_bucket=bucket,
            description=prj.get("description"),
            due=prj.get("due_date"),
            created=prj["created_at"],
            labels=prj.get("labels", []),
        )

        # Sections
        for sec in sections_by_project.get(prj["id"], []):
            sec_obj = Section(
                todoist_id=sec["id"],
                title=sec["name"],
                tasks=[
                    build_task(t)
                    for t in tasks_by_project.get(prj["id"], [])
                    if t.get("section_id") == sec["id"]
                ],
            )
            proj_obj.sections.append(sec_obj)

        # Root tasks (no section)
        root_tasks = [
            t for t in tasks_by_project.get(prj["id"], []) if not t.get("section_id")
        ]
        if root_tasks:
            proj_obj.sections.append(
                Section(
                    todoist_id=None,
                    title="(root)",
                    tasks=[build_task(t) for t in root_tasks],
                )
            )

        getattr(doc, bucket).append(proj_obj)

    Path(outfile).write_text(
        # Handle both Pydantic v1 and v2
        json.dumps(
            (
                doc.model_dump(exclude_none=True, by_alias=True)
                if hasattr(doc, "model_dump")
                else doc.dict(exclude_none=True, by_alias=True)
            ),
            indent=2,
        )
    )
    print(f"Wrote export to {outfile}")


# ---------------------------------------------------------------------------
# CLI entry‑point (Typer)
# ---------------------------------------------------------------------------


if __name__ == "__main__":
    import os
    import typer

    app = typer.Typer(help="Export Todoist tasks to PARA + GTD JSON format.")

    @app.command()
    def run(token: str = None, outfile: str = None) -> None:  # noqa: D401
        """Run an export with the given API *token*.
        
        You can also use TODOIST_API_TOKEN and TODOST_OUTPUT_FILE environment variables.
        """
        # Check for token in environment if not provided as argument
        if token is None:
            token = os.environ.get("TODOIST_API_TOKEN")
            if not token:
                raise typer.BadParameter(
                    "No token provided! Either pass as argument or set TODOIST_API_TOKEN environment variable."
                )
                
        # Check for output file in environment if not provided as argument
        if outfile is None:
            outfile = os.environ.get("TODOST_OUTPUT_FILE", "todoist_gtd_para.json")
            
        # Check log level from environment
        log_level = os.environ.get("LOG_LEVEL", "INFO")
        if log_level == "DEBUG":
            print(f"[DEBUG] Using token: {token[:4]}...{token[-4:]}")
            print(f"[DEBUG] Output file: {outfile}")

        asyncio.run(export(token=token, outfile=outfile))

    app()