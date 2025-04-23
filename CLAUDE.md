# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build Commands

- Build/run: `bazel run //path/to/target` (e.g., `bazel run //python/hello_python`)
- Test all: `bazel test //...`
- Integration tests: `bazel test --test_tag_filters=integ`
- Format code: Use pre-commit hooks (`pre-commit run --all-files`)
- Lint TypeScript: `cd ts && npx eslint .`
- Lint Python: `ruff check`

## Agentic Workflows

When working with Claude, use these three core instructions to maximize agentic capabilities:

### 1. Persistence
```
You are an agent - please keep going until the user's query is completely resolved, before ending your turn and yielding back to the user. Only terminate your turn when you are sure that the problem is solved.
```

### 2. Tool-calling
```
If you are not sure about file content or codebase structure pertaining to the user's request, use your tools to read files and gather the relevant information: do NOT guess or make up an answer.
```

### 3. Planning
```
You MUST plan extensively before each function call, and reflect extensively on the outcomes of the previous function calls. DO NOT do this entire process by making function calls only, as this can impair your ability to solve the problem and think insightfully.
```

### Effective Code Modification
When modifying code, use one of these diff formats for higher success rates:

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

## Code Style

- **TypeScript**: Follow ESLint config - imports ordered (builtin→external→internal→parent→sibling→index) with newlines between groups
- **Python**: Follow Ruff rules (PEP8 + additional checks) with 88-char line length
- **Bazel**: Use buildifier for formatting
- **Naming**: snake_case for Python, camelCase for TypeScript; unused vars prefixed with underscore
- **Errors**: Avoid console.log (only warn/error); add type annotations
- **Features**: Go/Rust are optional (use `--//features:go` or `--//features:rust` flags)

## Cost Efficiency

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
- **Special Commands**: `claude mcp` command for MCP capabilities

## Prompting Guide for Claude Code CLI

A quick‑start reference for using the Claude Code agent in your terminal.

### Starter Tasks

```bash
# See the built‑in help
claude --help

# Ask Claude what it can do
claude "write 2‑3 sentences on what you can do"
```

#### First hands‑on example – generate an HTML page

```bash
mkdir first-task && cd first-task
git init
claude "Create a file poem.html that renders a poem about the nature of intelligence and programming by you, Claude. Add some elegant CSS so it looks like it's framed on a wall."
```

Claude starts in **interactive mode** by default. Accept each proposed edit with **`y`** until the task is complete, then open _poem.html_ in a browser.

### Custom Instructions ("memories")

Claude Code injects Markdown‑based memory files into every session.

| Scope                | File                  | Purpose                                                                                    |
| -------------------- | --------------------- | ------------------------------------------------------------------------------------------ |
| **User‑level**       | `~/.claude/CLAUDE.md` | Global personal defaults (shell tips, editor prefs, safety rules). Keep it concise.        |
| **Project (shared)** | `CLAUDE.md`           | Team conventions, repo layout, command policies. Autodetected from the Git root.           |
| **Project (local)**  | `CLAUDE.local.md`     | Private, project‑specific notes that shouldn't be shared (e.g. test URLs). Ignored by git. |

> **Tip:** Start any line with `#` inside the REPL to save it as a memory entry without leaving the terminal.

### Prompting Techniques

Claude supports different patterns for various task sizes.

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

Give Claude more autonomy by seeding a **`.claude/`** workspace:

1. Add high‑level requirements docs inside `.claude/`
2. Instruct Claude to persist plans as it works, e.g. `.claude/plan_2025‑04‑23.md`
3. Ask it to update the main `README.md` with a dated changelog

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
