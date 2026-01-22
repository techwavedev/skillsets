#!/usr/bin/env python3
"""
Skills Catalog Updater

Scans the skills directory and updates SKILLS_CATALOG.md with current skill information.
Run this script after creating, modifying, or deleting any skill.

Usage:
    update_catalog.py --skills-dir <path>

Examples:
    update_catalog.py --skills-dir skills/
    update_catalog.py --skills-dir /path/to/skills

Exit Codes:
    0 - Success
    1 - Invalid arguments
    2 - Skills directory not found
    3 - Catalog file error
"""

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path


def parse_skill_frontmatter(skill_md_path: Path) -> dict:
    """
    Parse YAML frontmatter from a SKILL.md file.
    
    Returns:
        dict with 'name' and 'description' keys, or None if parsing fails.
    """
    try:
        content = skill_md_path.read_text()
    except Exception as e:
        print(f"  ⚠️  Could not read {skill_md_path}: {e}")
        return None
    
    # Check for YAML frontmatter
    if not content.startswith('---'):
        print(f"  ⚠️  No YAML frontmatter in {skill_md_path}")
        return None
    
    # Extract frontmatter
    parts = content.split('---', 2)
    if len(parts) < 3:
        print(f"  ⚠️  Invalid YAML frontmatter in {skill_md_path}")
        return None
    
    frontmatter = parts[1].strip()
    
    # Parse simple YAML (name and description only)
    result = {}
    for line in frontmatter.split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()
            if key in ('name', 'description'):
                result[key] = value
    
    return result if 'name' in result else None


def scan_skills(skills_dir: Path) -> list:
    """
    Scan the skills directory for all skills.
    
    Returns:
        List of skill info dicts with name, description, location, scripts, references.
    """
    skills = []
    
    for item in sorted(skills_dir.iterdir()):
        if not item.is_dir():
            continue
        
        skill_md = item / 'SKILL.md'
        if not skill_md.exists():
            print(f"  ⚠️  Skipping {item.name}: no SKILL.md found")
            continue
        
        frontmatter = parse_skill_frontmatter(skill_md)
        if not frontmatter:
            print(f"  ⚠️  Skipping {item.name}: could not parse frontmatter")
            continue
        
        # Gather skill info
        skill_info = {
            'name': frontmatter.get('name', item.name),
            'description': frontmatter.get('description', ''),
            'dir_name': item.name,
            'location': f"skills/{item.name}/",
            'scripts': [],
            'references': [],
            'has_assets': False,
            'parent': None,
        }
        
        # Check for scripts
        scripts_dir = item / 'scripts'
        if scripts_dir.exists() and scripts_dir.is_dir():
            for script in sorted(scripts_dir.glob('*.py')):
                if script.name != '__init__.py' and not script.name.startswith('example'):
                    skill_info['scripts'].append(script.name)
        
        # Check for references
        refs_dir = item / 'references'
        if refs_dir.exists() and refs_dir.is_dir():
            for ref in sorted(refs_dir.glob('*.md')):
                if not ref.name.startswith('example'):
                    skill_info['references'].append(ref.name)
        
        # Check for assets
        assets_dir = item / 'assets'
        if assets_dir.exists() and assets_dir.is_dir():
            skill_info['has_assets'] = any(assets_dir.iterdir())
        
        # Detect parent skill from SKILL.md content
        try:
            content = skill_md.read_text()
            if 'Part of the' in content and 'skill family' in content:
                # Extract parent reference
                match = re.search(r'\[([Aa]ws)\s*(skill family|skill)\]', content)
                if match:
                    skill_info['parent'] = 'aws'
            elif '../aws/SKILL.md' in content:
                skill_info['parent'] = 'aws'
        except Exception:
            pass
        
        skills.append(skill_info)
        print(f"  ✅ Found skill: {skill_info['name']}")
    
    return skills


def generate_skill_entry(skill: dict) -> str:
    """Generate a markdown section for a single skill."""
    lines = []
    
    # Title
    title = skill['name'].replace('-', ' ').title()
    if skill['name'] == 'aws':
        title = 'AWS (Hub)'
    lines.append(f"### {title}")
    lines.append("")
    
    # Property table
    lines.append("| Property | Value |")
    lines.append("| -------- | ----------------------- |")
    lines.append(f"| **Name** | `{skill['name']}` |")
    lines.append(f"| **Path** | `{skill['location']}` |")
    
    if skill['parent']:
        parent_title = skill['parent'].replace('-', ' ').title()
        parent_anchor = skill['parent'].replace('-', '')
        lines.append(f"| **Parent** | [{parent_title}](#{parent_anchor}) |")
    elif skill['name'] == 'aws':
        lines.append("| **Type** | Router |")
    else:
        # Determine type
        desc = skill['description'].lower()
        if 'template' in desc or 'example' in desc:
            skill_type = 'Template'
        elif 'create' in desc and 'skill' in desc:
            skill_type = 'Utility'
        else:
            skill_type = 'Standalone'
        lines.append(f"| **Type** | {skill_type} |")
    
    lines.append("")
    
    # Purpose (short description)
    desc = skill['description']
    if desc.startswith('[TODO'):
        desc = '*[Description not yet provided]*'
    # Truncate long descriptions
    if len(desc) > 200:
        desc = desc[:197] + '...'
    lines.append(f"**Purpose:** {desc}")
    lines.append("")
    
    # Scripts - compact list format
    if skill['scripts']:
        lines.append("**Scripts:**")
        lines.append("")
        for script in skill['scripts']:
            # Create friendly name from script filename
            friendly_name = script.replace('.py', '').replace('_', ' ').title()
            lines.append(f"- `{script}` — {friendly_name}")
        lines.append("")
    
    # References - compact inline format
    if skill['references']:
        refs_str = ', '.join([f"`{ref}`" for ref in skill['references']])
        lines.append(f"**References:** {refs_str}")
    
    # Assets
    if skill['has_assets']:
        lines.append(f"**Assets:** `config.template.json`")
    
    lines.append("")
    lines.append("---")
    lines.append("")
    
    return '\n'.join(lines)


def generate_catalog(skills: list) -> str:
    """Generate the complete SKILLS_CATALOG.md content in streamlined format."""
    
    # Build quick reference table rows
    quick_ref_rows = []
    for skill in sorted(skills, key=lambda s: s['name']):
        name = skill['name']
        anchor = name.replace('-', '-')
        
        # Determine type
        if skill['name'] == 'aws':
            skill_type = 'Router'
        elif skill['parent']:
            skill_type = 'Sub-skill'
        else:
            skill_type = 'Standalone'
        
        # Extract domain from description or use generic
        desc = skill['description']
        if 'memory' in desc.lower() or 'cache' in desc.lower() or 'rag' in desc.lower():
            domain = 'AI/ML'
        elif 'template' in desc.lower() or 'example' in desc.lower():
            domain = 'Learning'
            skill_type = 'Template'
        elif 'create' in desc.lower() and 'skill' in desc.lower():
            domain = 'Development'
            skill_type = 'Utility'
        elif 'aws' in name.lower():
            domain = 'Cloud'
        else:
            domain = 'General'
        
        # Create short use-case
        short_desc = desc[:40] + '...' if len(desc) > 43 else desc
        # Simplify to key action
        if 'template' in desc.lower():
            use_for = 'Skill structure demo'
        elif 'semantic' in desc.lower() or 'cache' in desc.lower():
            use_for = 'Semantic cache, RAG, memory'
        elif 'create' in desc.lower() and 'skill' in desc.lower():
            use_for = 'Create new skills'
        else:
            use_for = short_desc
        
        quick_ref_rows.append(f"| [`{name}`](#{anchor}) | {skill_type} | {domain} | {use_for} |")
    
    # Build architecture tree
    arch_lines = []
    for skill in sorted(skills, key=lambda s: s['name']):
        comment = ""
        if 'template' in skill['description'].lower() or 'example' in skill['description'].lower():
            comment = "# Template (start here!)"
        elif 'memory' in skill['description'].lower() or 'cache' in skill['description'].lower():
            comment = "# Semantic caching & RAG"
        arch_lines.append(f"│  ├── {skill['dir_name']}/        {comment}".rstrip())
    
    # Header section
    header = """# 🧠 Skills Catalog

> **Modular AI Agent Skills Framework** — Extend agent capabilities with specialized knowledge and tools
>
> Created by **Elton Machado** • Licensed under [Apache 2.0](../LICENSE)

---

## 📋 Quick Reference

| Skill                             | Type       | Domain      | Use For                     |
| --------------------------------- | ---------- | ----------- | --------------------------- |
"""
    
    header += '\n'.join(quick_ref_rows)
    
    header += """

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    SKILL FRAMEWORK                          │
├─────────────────────────────────────────────────────────────┤
│  skills/                                                    │
"""
    
    for skill in sorted(skills, key=lambda s: s['name']):
        comment = ""
        if 'template' in skill['description'].lower() or 'example' in skill['description'].lower():
            comment = "        # Template (start here!)"
        elif 'memory' in skill['description'].lower() or 'cache' in skill['description'].lower():
            comment = "        # Semantic caching & RAG"
        header += f"│  ├── {skill['dir_name']}/{comment}\n"
    
    header += """│  └── SKILLS_CATALOG.md     # This file                      │
│                                                             │
│  skill-creator/            # Skill creation toolkit         │
└─────────────────────────────────────────────────────────────┘
```

---

## 📦 Skills

"""
    
    # Generate skill entries
    skill_entries = []
    
    # Sort: hub skills first, then standalone, then sub-skills
    def sort_key(s):
        if s['name'] == 'aws':
            return ('0', s['name'])
        elif not s['parent']:
            return ('1', s['name'])
        else:
            return ('2', s['name'])
    
    for skill in sorted(skills, key=sort_key):
        skill_entries.append(generate_skill_entry(skill))
    
    # Footer
    footer = """## 🚀 Usage

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
"""
    
    return header + '\n'.join(skill_entries) + footer


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--skills-dir', required=True, help='Path to skills directory')
    parser.add_argument('--output', help='Output path (default: <skills-dir>/SKILLS_CATALOG.md)')
    parser.add_argument('--json', action='store_true', help='Also output JSON summary')
    args = parser.parse_args()
    
    skills_dir = Path(args.skills_dir).resolve()
    
    if not skills_dir.exists() or not skills_dir.is_dir():
        print(f"❌ Error: Skills directory not found: {skills_dir}")
        sys.exit(2)
    
    print(f"🔍 Scanning skills in: {skills_dir}")
    print()
    
    # Scan for skills
    skills = scan_skills(skills_dir)
    
    if not skills:
        print("\n⚠️  No valid skills found.")
        sys.exit(0)
    
    print(f"\n📚 Found {len(skills)} skill(s)")
    
    # Generate catalog
    catalog_content = generate_catalog(skills)
    
    # Determine output path
    output_path = Path(args.output) if args.output else skills_dir / 'SKILLS_CATALOG.md'
    
    try:
        output_path.write_text(catalog_content)
        print(f"✅ Catalog updated: {output_path}")
    except Exception as e:
        print(f"❌ Error writing catalog: {e}")
        sys.exit(3)
    
    # Optional JSON output
    if args.json:
        json_path = output_path.with_suffix('.json')
        try:
            json_path.write_text(json.dumps(skills, indent=2))
            print(f"✅ JSON summary: {json_path}")
        except Exception as e:
            print(f"⚠️  Could not write JSON: {e}")
    
    print("\n✅ Catalog update complete!")
    sys.exit(0)


if __name__ == '__main__':
    main()
