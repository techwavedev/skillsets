# 🤖 Agent Instructions

> **Reliable AI-OS Architecture** — Determinism over probability
>
> Created by **Elton Machado** • Licensed under [Apache 2.0](LICENSE)

---

## 🎯 Core Philosophy

LLMs are probabilistic, but business logic requires consistency. This system fixes that mismatch by **pushing complexity into deterministic code**.

> **Why it matters:** 90% accuracy per step = 59% success over 5 steps.  
> **Solution:** Minimize probabilistic steps by delegating execution to reliable scripts.

---

## 🏗️ The 3-Layer Architecture

```
┌────────────────────────────────────────────────────────────────┐
│                         INTENT                                 │
│                      (Directives)                              │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  directives/*.md — SOPs defining goals, inputs, outputs  │  │
│  └──────────────────────────────────────────────────────────┘  │
├────────────────────────────────────────────────────────────────┤
│                       ORCHESTRATION                            │
│                        (Agent)                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Read directives → Invoke scripts → Handle errors        │  │
│  │  Ask for clarification → Update directives with learnings│  │
│  └──────────────────────────────────────────────────────────┘  │
├────────────────────────────────────────────────────────────────┤
│                        EXECUTION                               │
│                       (Scripts)                                │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  execution/*.py — Deterministic, tested, idempotent      │  │
│  │  skills/*/scripts/ — Modular capability scripts          │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────┘
```

| Layer             | Location                          | Purpose                                 |
| ----------------- | --------------------------------- | --------------------------------------- |
| **Directives**    | `directives/`                     | SOPs defining what to accomplish        |
| **Orchestration** | _Agent_                           | Intelligent routing and decision-making |
| **Execution**     | `execution/`, `skills/*/scripts/` | Deterministic Python scripts            |

---

## 📋 Directives

Directives are SOPs in Markdown that bridge human intent to machine execution:

```markdown
# directives/example_task.md

## Goal

What needs to be accomplished

## Inputs

- Required data and parameters
- Configuration files

## Execution

1. Run `execution/step_one.py --param value`
2. Run `execution/step_two.py --input .tmp/output.json`

## Outputs

- Expected deliverables and location

## Edge Cases

- Rate limiting: Auto-retry with backoff
- Auth required: Skip and alert user
```

---

## ⚙️ Operating Principles

### 1. Check Before Creating

| Priority | Action                                  |
| -------- | --------------------------------------- |
| 1st      | Check `execution/` for existing scripts |
| 2nd      | Review relevant directive for workflows |
| 3rd      | Search Knowledge Items for patterns     |

Only create new scripts when truly necessary.

### 2. Self-Anneal on Errors

```
ERROR DETECTED
    ↓
1. Read full error message and stack trace
    ↓
2. Diagnose root cause
    ↓
3. Fix script or adjust parameters
    ↓
4. Test fix (⚠️ confirm if paid APIs/side effects)
    ↓
5. Update directive with learnings
    ↓
SYSTEM IS NOW STRONGER
```

### 3. Update Directives as You Learn

- API constraints, rate limits
- Better approaches, optimizations
- Common errors and solutions
- Timing expectations

### 4. Validate Before Delivering

- ✅ Outputs exist and are accessible
- ✅ Data quality spot-checked
- ✅ Deliverables in expected location

---

## 📁 Directory Structure

```
project/
├── .agent/workflows/     # Quick-reference workflows
├── .env                  # Environment variables
├── .tmp/                 # Intermediate files (regenerable)
├── directives/           # SOPs in Markdown
├── execution/            # Deterministic Python scripts
├── skills/               # Modular capabilities
│   ├── SKILLS_CATALOG.md # Complete skill documentation
│   └── <skill>/
│       ├── SKILL.md      # Instructions + triggers
│       ├── scripts/      # Executable tools
│       └── references/   # On-demand documentation
├── skill-creator/        # Skill creation toolkit
└── AGENTS.md             # This file
```

---

## 🧠 Skills System

Skills are modular packages that extend agent capabilities.

| Resource           | Location                                               |
| ------------------ | ------------------------------------------------------ |
| **Skills Catalog** | [`skills/SKILLS_CATALOG.md`](skills/SKILLS_CATALOG.md) |
| **Skill Creator**  | `skill-creator/SKILL_skillcreator.md`                  |

### Commands

```bash
# Create a new skill
python3 skill-creator/scripts/init_skill.py <name> --path skills/

# Update skills catalog (MANDATORY after any skill change)
python3 skill-creator/scripts/update_catalog.py --skills-dir skills/
```

---

## 🔧 Script Template

```python
#!/usr/bin/env python3
"""
Script: script_name.py
Purpose: Brief description

Usage:
    python script_name.py --input <file> --output <file>

Exit Codes:
    0 - Success
    1 - Invalid arguments
    2 - Input not found
    3 - Network error
    4 - Processing error
"""

import argparse
import json
import sys
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()

    try:
        result = process(args.input)
        Path(args.output).write_text(json.dumps(result, indent=2))
        print(json.dumps({"status": "success", "output": args.output}))
        sys.exit(0)
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}), file=sys.stderr)
        sys.exit(4)

if __name__ == '__main__':
    main()
```

---

## 🏷️ Naming Conventions

| Type       | Convention         | Example                     |
| ---------- | ------------------ | --------------------------- |
| Scripts    | `verb_noun.py`     | `scrape_website.py`         |
| Directives | `noun_or_task.md`  | `competitor_analysis.md`    |
| Temp files | Descriptive + date | `.tmp/data_2024-01-19.json` |

---

## 🔄 Workflow Quick Reference

Create workflows in `.agent/workflows/`:

```markdown
# .agent/workflows/example.md

---

## description: Brief task description

1. Verify `.env` contains required keys
2. Run `python execution/step_one.py`
   // turbo
3. Run `python execution/step_two.py`
4. Verify output and share with user
```

> **Note:** `// turbo` auto-runs that step. `// turbo-all` auto-runs all command steps.

---

## 📝 Summary

You are the intelligent orchestrator between human intent and deterministic execution:

| Role           | Action                           |
| -------------- | -------------------------------- |
| **Understand** | Read directives before acting    |
| **Execute**    | Call scripts in the right order  |
| **Adapt**      | Handle errors gracefully         |
| **Learn**      | Update directives with knowledge |
| **Deliver**    | Ensure outputs reach destination |

**Be pragmatic. Be reliable. Self-anneal.**

---

## 📜 License & Attribution

**Apache License 2.0** — Copyright © 2026 Elton Machado

See [LICENSE](LICENSE) and [NOTICE](NOTICE) for full details.

---

<div align="center">

**[📚 Skills Catalog](skills/SKILLS_CATALOG.md)** • **[🛠️ Create Skills](skill-creator/SKILL_skillcreator.md)**

_Reliable AI-OS by Elton Machado_

</div>
