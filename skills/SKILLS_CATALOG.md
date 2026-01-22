# 🧠 Skills Catalog

> **Modular AI Agent Skills Framework** — Extend agent capabilities with specialized knowledge and tools
>
> Created by **Elton Machado** • Licensed under [Apache 2.0](../LICENSE)

---

## 📋 Quick Reference

| Skill                             | Type       | Domain      | Use For                     |
| --------------------------------- | ---------- | ----------- | --------------------------- |
| [`example-skill`](#example-skill) | Template | Learning | Skill structure demo |
| [`qdrant-memory`](#qdrant-memory) | Standalone | AI/ML | Semantic cache, RAG, memory |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    SKILL FRAMEWORK                          │
├─────────────────────────────────────────────────────────────┤
│  skills/                                                    │
│  ├── example-skill/        # Template (start here!)
│  ├── qdrant-memory/        # Semantic caching & RAG
│  └── SKILLS_CATALOG.md     # This file                      │
│                                                             │
│  skill-creator/            # Skill creation toolkit         │
└─────────────────────────────────────────────────────────────┘
```

---

## 📦 Skills

### Example Skill

| Property | Value |
| -------- | ----------------------- |
| **Name** | `example-skill` |
| **Path** | `skills/example-skill/` |
| **Type** | Template |

**Purpose:** Template skill demonstrating the complete Skillsets framework structure. Use as a reference when creating new skills for AI agents.

**Scripts:**

- `calculate.py` — Calculate
- `format_data.py` — Format Data
- `greet.py` — Greet

**References:** `patterns.md`
**Assets:** `config.template.json`

---

### Qdrant Memory

| Property | Value |
| -------- | ----------------------- |
| **Name** | `qdrant-memory` |
| **Path** | `skills/qdrant-memory/` |
| **Type** | Standalone |

**Purpose:** "Intelligent token optimization through Qdrant-powered semantic caching and long-term memory. Use for (1) Semantic Cache - avoid LLM calls entirely for semantically similar queries with 100% token ...

**Scripts:**

- `benchmark_token_savings.py` — Benchmark Token Savings
- `embedding_utils.py` — Embedding Utils
- `hybrid_search.py` — Hybrid Search
- `init_collection.py` — Init Collection
- `memory_retrieval.py` — Memory Retrieval
- `semantic_cache.py` — Semantic Cache
- `test_skill.py` — Test Skill

**References:** `advanced_patterns.md`, `collection_schemas.md`, `complete_guide.md`, `embedding_models.md`

---
## 🚀 Usage

### Automatic Triggering

Skills are automatically triggered based on task context matching skill descriptions.

### Explicit Invocation

```
"Use the <skill-name> skill to <task>"
```

### Skill Structure

```
skill-name/
├── SKILL.md           # (required) Main instruction file
├── scripts/           # (optional) Executable scripts
├── references/        # (optional) Documentation
└── assets/            # (optional) Templates, images
```

---

## 🛠️ Development

### Create New Skill

```bash
# 1. Start from the example-skill template
cp -r skills/example-skill skills/my-new-skill

# 2. Or use the skill-creator
python skill-creator/scripts/init_skill.py my-new-skill --path skills/
```

### Update This Catalog

```bash
python skill-creator/scripts/update_catalog.py --skills-dir skills/
```

---

## 📜 License & Attribution

**Apache License 2.0** — Copyright © 2026 Elton Machado

When using, modifying, or distributing:

1. ✅ Retain the `LICENSE` and `NOTICE` files
2. ✅ Include attribution: _"AI Agent Skills Framework by Elton Machado"_
3. ✅ Keep copyright notices intact

See [LICENSE](../LICENSE) and [NOTICE](../NOTICE) for full details.

---

<div align="center">

_Part of the [3-Layer Architecture](../AGENTS.md) for reliable AI agent operations_

</div>
