# 🧠 Skillsets — AI Agent Skills Framework

> **Extend AI agent capabilities with modular, specialized skills**

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Skills](https://img.shields.io/badge/Skills-3-green.svg)](skills/SKILLS_CATALOG.md)

---

## ✨ Overview

**Skillsets** is a modular framework for extending AI agent capabilities with specialized knowledge, workflows, and tools. Each skill is a self-contained package that can be triggered automatically or invoked explicitly.

### Key Features

- 🔌 **Plug-and-Play Skills** — Drop-in modules for specialized domains
- 🎯 **Auto-Triggering** — Skills activate based on task context
- 📚 **Rich Documentation** — References, scripts, and examples included
- ⚡ **Token Optimization** — Semantic caching and memory management

---

## 📦 Available Skills

| Skill           | Type       | Use For                     |
| --------------- | ---------- | --------------------------- |
| `example-skill` | Template   | Learn skill structure       |
| `qdrant-memory` | Standalone | Semantic cache, RAG, memory |
| `skill-creator` | Utility    | Create new skills           |

👉 **[View Full Catalog](skills/SKILLS_CATALOG.md)**

---

## 🚀 Quick Start

### Use a Skill

Skills are automatically triggered based on your request:

```
"Cache this response for similar queries"
→ Triggers: qdrant-memory skill

"Create a new skill for my project"
→ Triggers: skill-creator
```

Or invoke explicitly:

```
"Use the example-skill to greet me"
```

### Create a New Skill

```bash
# Copy from template
cp -r skills/example-skill skills/my-new-skill

# Or use the skill-creator
python skill-creator/scripts/init_skill.py my-new-skill --path skills/
```

---

## 🏗️ Skill Structure

```
skill-name/
├── SKILL.md           # Main instruction file (required)
├── scripts/           # Executable utilities
├── references/        # Documentation and guides
└── assets/            # Templates, configs, images
```

---

## 📜 License

This project is licensed under the **Apache License 2.0** — see [LICENSE](LICENSE) for details.

**Copyright © 2026 Elton Machado**

### Attribution Requirements

When using, modifying, or distributing this framework, you must:

1. ✅ Retain the `LICENSE` and `NOTICE` files in any redistribution
2. ✅ Include attribution: _"AI Agent Skills Framework by Elton Machado"_
3. ✅ Keep all copyright notices intact

See [NOTICE](NOTICE) for full attribution requirements.

---

## 🤝 Contributing

Contributions are welcome! Please ensure you:

1. Follow the skill structure guidelines
2. Update the [SKILLS_CATALOG.md](skills/SKILLS_CATALOG.md) after adding skills
3. Include appropriate documentation and scripts

---

## 👤 Author

**Elton Machado**

---

<div align="center">

**[📚 Skills Catalog](skills/SKILLS_CATALOG.md)** • **[🐛 Report Issue](https://github.com/techwavedev/skillsets/issues)** • **[💡 Request Feature](https://github.com/techwavedev/skillsets/issues)**

Made with ❤️ by Elton Machado

</div>
