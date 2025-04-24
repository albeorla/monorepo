# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Structure

This monorepo contains multiple language-specific projects:

- `/python/` - Python projects including hello_python and todost
- `/go/` - Go projects including hello_go
- `/rust/` - Rust projects including hello_rust
- `/ts/` - TypeScript projects including hello_ts

## Agentic Workflows

When working with Claude, use these core instructions for effective agentic problem-solving:

### 1. Persistence

Always see tasks through to completion before yielding control:

```
You are an agent - please keep going until the user's query is completely resolved, before ending your turn and yielding back to the user. Only terminate your turn when you are sure that the problem is solved.
```

### 2. Information Gathering

Avoid guesswork and use available tools:

```
If you are not sure about file content or codebase structure pertaining to the user's request, use your tools to read files and gather the relevant information: do NOT guess or make up an answer.
```

### 3. Planning and Action Cycles

Alternate between planning and acting, returning to planning whenever needed:

```
You MUST plan extensively before each function call, and reflect extensively on the outcomes of the previous function calls. DO NOT do this entire process by making function calls only, as this can impair your ability to solve the problem and think insightfully. Feel free to transition between planning and action phases as needed - return to planning whenever you discover new information or complications.
```

### Problem-Solving Strategy

Follow this flexible approach for complex tasks, freely transitioning between planning and action phases as needed:

#### Initial Phase

1. Understand the problem deeply
2. Investigate the codebase thoroughly

#### Planning Phase (enter/return to this phase any time)

3. Develop or refine a step-by-step plan:
   - Start with `mcp__softwareplanner__start_planning` to define the goal
   - Break down work into tasks with `mcp__softwareplanner__add_todo` (include title, description, complexity)
   - Review all tasks with `mcp__softwareplanner__get_todos`
   - Save the plan with `mcp__softwareplanner__save_plan`
   - Return to planning any time you discover new requirements or complications

#### Action Phase (enter/return to this phase any time)

4. Implement changes incrementally:
   - Work through todos in complexity order
   - Mark progress with `mcp__softwareplanner__update_todo_status`
   - Remove tasks if needed with `mcp__softwareplanner__remove_todo`
5. Test frequently after each change
6. Debug as needed (use sequentialthinking MCP tool for complex problems)

#### Finalization Phase

7. Update documentation to reflect changes
8. Iterate until the solution is complete and verified
9. Update project tracking documents in docs/planning/ and docs/reports/ directories

### Effective Code Modification

When modifying code, use these diff formats for higher success rates:

```
<edit>
<file>path/to/file.py</file>
<old_code>
def function():
    pass
</old_code>
<new_code>
def function():
    return "implementation"
</new_code>
</edit>
```

Or alternatively:

```
path/to/file.py
>>>>>>> SEARCH
def function():
    pass
=======
def function():
    return "implementation"
<<<<<<< REPLACE
```

## Build System

This project uses Bazel as the build system. When making changes, ensure they comply with Bazel build conventions:

- All new directories should include a BUILD.bazel file
- Follow existing dependency patterns for each language

### Common Build Commands

- Build/run: `bazel run //path/to/target` (e.g., `bazel run //python/hello_python`)
- Test all: `bazel test //...`
- Integration tests: `bazel test --test_tag_filters=integ`
- Format code: Use pre-commit hooks (`pre-commit run --all-files`)
- Lint TypeScript: `cd ts && npx eslint .`
- Lint Python: `ruff check`
- Optional features: Use `--//features:go` or `--//features:rust` flags

## Coding Conventions

- Python:
  - Follow PEP 8 style guidelines
  - Line length 88 characters
  - Follow Ruff rules (PEP8 + additional checks)
  - Use snake_case for naming
  - Prefix unused variables with underscore
- TypeScript:
  - Follow the conventions in existing .ts files and comply with eslint rules (.eslintrc.js)
  - Use camelCase for naming
  - Order imports: builtin→external→internal→parent→sibling→index with newlines between groups
  - Add type annotations
  - Avoid console.log (use warn/error only)
- Go: Follow standard Go conventions with gofmt
- Rust: Follow the Rust style guide and use cargo fmt
- Bazel: Use buildifier for formatting

## Testing

- Add tests alongside new features
- Run appropriate tests for the language you're modifying
- Pytest is used for Python testing

## Documentation Practices

- Keep documentation in sync with code changes
- Update the following files after completing tasks:
  - `docs/planning/sprints/sprint_YYYY-MM-DD.md`: Mark completed tasks and update progress metrics
  - `docs/planning/dashboard.md`: Update progress percentages and milestone status
  - `docs/reports/work_summary_YYYY-MM-DD.md`: Create detailed summaries of completed work
- Create dedicated documentation for:
  - New modules (README.md files)
  - New tools or scripts (usage guides)
  - Configuration changes (update relevant docs)
- Include documentation updates in the same commit as code changes
- Reference PRD requirements (e.g., F-1, F-5) in documentation updates

## CI/CD

- Changes should pass CI checks defined in .github/workflows
- Pre-commit hooks are defined in .pre-commit-config.yaml
- Cost efficiency requirements:
  - CI cost per PR must be ≤ $0.10
  - Keep build times under 60 seconds when possible

## Claude Code Usage

- **Installation**: `npm install -g @anthropic-ai/claude-code` (do NOT use `sudo`)
- **Default Model**: `claude-3-7-sonnet-20250219` (override with `ANTHROPIC_MODEL` env var)
- **Run Modes**: Interactive (default), Non-interactive (`--print` or `-p`)
- **CLI Flags**: `--json`, `--verbose`, `--dangerously-skip-permissions`
- **Memory Files**: `./CLAUDE.md`, `./CLAUDE.local.md`, `~/.claude/CLAUDE.md`, `~/.claude/settings.json` for shared permissions
- **Extended Thinking**: Use "think" or "think hard" prompts for deeper reasoning
- **Slash Commands**:
  - `/bug`, `/help`, `/init`, `/cost`, `/compact`, `/vim`, `/memory`
  - `/clear`, `/doctor`, `/login`, `/logout`, `/pr_comments`, `/review`, `/terminal-setup`
- **MCP Features**:
  - Check status: `claude mcp`
  - Software planning: Use `claude mcp` for structured development planning with these tools:
    - `mcp__softwareplanner__start_planning`: Begin a new planning session with a goal
    - `mcp__softwareplanner__add_todo`: Add tasks with title, description, and complexity
    - `mcp__softwareplanner__get_todos`: List all current tasks
    - `mcp__softwareplanner__update_todo_status`: Mark tasks complete/incomplete
    - `mcp__softwareplanner__remove_todo`: Remove a task by ID
    - `mcp__softwareplanner__save_plan`: Save the current plan
  - Sequential thinking: Use `mcp__sequentialthinking__sequentialthinking` for step-by-step problem solving and complex reasoning tasks
  - Web search: Connect to search MCP servers for real-time information:
    - [Exa](https://github.com/exa-labs/exa-mcp-server): AI-powered web search
    - [Brave Search](https://github.com/modelcontextprotocol/servers/tree/main/src/brave-search): Privacy-respecting search
  - Browser automation:
    - [Microsoft Playwright](https://github.com/microsoft/playwright-mcp): Official Microsoft browser automation
    - [BrowserMCP](https://github.com/browsermcp/mcp): Control your local Chrome browser
  - Knowledge bases:
    - [Memory](https://github.com/modelcontextprotocol/servers/tree/main/src/memory): Persistent memory across sessions
  - Whitelist all MCP tools in your configuration for seamless workflow

## Prompting Guide for Claude

### Task Patterns

#### Small Requests

When the change is tiny and surgical, be **specific**:

```bash
claude "Modify the discount function utils/priceUtils.ts to apply a 10% discount"
```

Key principles:

- Name the exact file / function
- State both the change **and** the expected behaviour
- Stay in interactive mode for rapid feedback

#### Medium Tasks

Put multi‑paragraph instructions in a file and pipe it:

```bash
claude "$(cat task_description.md)"
```

Include:

- A one‑sentence goal
- Relevant context (or rely on `CLAUDE.md`)
- Any files Claude should read, edit, or mimic
- How to report its work (e.g. _write what you changed to `final_output.md`_)

#### Large Projects / Agentic Workflows

Give Claude more autonomy by using a structured workflow, freely transitioning between planning and implementation as needed:

1. **Initial planning with MCP tools:**

   - Start with `mcp__softwareplanner__start_planning` to define the overall goal
   - Break down work into tasks with specific complexity ratings
   - Save the plan with `mcp__softwareplanner__save_plan`

2. **Document in structured directories:**

   - Add high‑level requirements docs inside `docs/planning/`
   - Persist plans as it works, e.g. `docs/planning/sprints/sprint_2025‑04‑23.md`
   - Track progress in `docs/planning/dashboard.md` with regular updates
   - Create work summaries in `docs/reports/work_summary_YYYY-MM-DD.md` after completing tasks
   - Store architectural decisions in `docs/decisions/decisions.md`

3. **Iterative implementation cycle:**

   - Work through todos in complexity order
   - Use explicit planning between tool calls
   - Persist progress with `mcp__softwareplanner__update_todo_status`
   - **Return to planning phase** whenever you discover:
     - New requirements
     - Technical complications
     - Better approaches
     - Need to refactor tasks

4. **Documentation and reporting:**
   - Update the main `README.md` with a dated changelog
   - Create detailed work summaries with implementation details

> **Important**: You should freely alternate between planning and implementation phases throughout the project lifecycle. Don't hesitate to return to the planning phase to refine the approach as your understanding evolves.

### Modes of Interaction

| Mode                             | Launch command                         | Typical use‑case                     |
| -------------------------------- | -------------------------------------- | ------------------------------------ |
| **Interactive REPL** (default)   | `claude` or `claude "query"`           | Exploratory work, step‑by‑step fixes |
| **Print‑only / non‑interactive** | `claude -p "query"`                    | CI pipelines, scripts, quick answers |
| **Pipe input**                   | `cat foo.txt \| claude -p "summarise"` | Explain logs or diff output          |

Add `--json` for machine‑readable output, `--verbose` for full logs, or `--dangerously-skip-permissions` in locked‑down build agents.

### Memory‑driven Workflows

- Use `/memory` to open any memory file in your editor
- Structure entries as bullet points under headings
- Review memories periodically—stale guidance can confuse the agent

### Permission & Security Quick‑reference

- Safe reads (ls, grep, file‑read) require **no** approval
- Mutating tools (bash, edit, write) prompt for approval the first time per session—unless:
  - The command matches an allow‑rule in `allowedTools` (`claude config add allowedTools "Bash(npm test:*)"`)
  - You approve with "Yes, don't ask again"

For automated contexts, pre‑populate `.claude/settings.json` with allow‑rules and run with `--print`.

### Cheat‑sheet

```bash
# Install globally
npm install -g @anthropic-ai/claude-code

# Configure a safe npm prefix if needed
npm config set prefix ~/.npm-global

# Authenticate once
claude   # follows OAuth flow

# Update
claude update
```

### Further Reading

- **Official docs:** https://docs.anthropic.com/s/claude-code
- **Troubleshooting / FAQs:** `claude /help`, `claude config list`, or the docs site
