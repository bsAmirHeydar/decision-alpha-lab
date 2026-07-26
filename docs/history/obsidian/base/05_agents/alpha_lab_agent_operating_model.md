---
title: "Alpha Lab Agent Operating Model"
type: agent_policy
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
status: "proposed"
---

# Alpha Lab Agent Operating Model

Agent آینده پروژه باید ابتدا research/knowledge/patch assistant باشد، نه live trading authority.

## Layering

```mermaid
graph TD
    U[User] --> O[Alpha Lab Orchestrator]
    O --> L[Obsidian Librarian]
    O --> E[Experiment Designer]
    O --> P[Patch Builder]
    O --> V[Validation Skeptic]
    O --> J[Journal Reviewer]
    L --> OBS[Obsidian Vault]
    E --> LAB[lab/]
    P --> GIT[Git Patch]
    V --> REP[reports + registry]
```

## Hard rules

1. Agent حق ارسال live order ندارد.
2. Agent حق افزایش risk ندارد.
3. Agent حق bypass کردن validation ندارد.
4. Agent باید هر تغییر را به diff و rollback plan وصل کند.
5. Agent باید هر experiment را به hypothesis و هر validation را به experiment وصل کند.
6. Agent باید negative result را حذف نکند؛ archive کند.
7. Agent باید برای هر claim مثبت baseline بخواهد.

## First useful agents

- [[docs/obsidian/05_agents/obsidian_librarian_agent|Obsidian Librarian Agent]]
- [[docs/obsidian/05_agents/experiment_designer_agent|Experiment Designer Agent]]
- [[docs/obsidian/05_agents/patch_builder_agent|Patch Builder Agent]]
- [[docs/obsidian/05_agents/validation_skeptic_agent|Validation Skeptic Agent]]
