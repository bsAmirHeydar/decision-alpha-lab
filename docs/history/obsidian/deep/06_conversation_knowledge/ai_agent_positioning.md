
---
type: agent_positioning
---

# AI Agent Positioning

## جای درست ایجنت

ایجنت باید اول «Chief Research Assistant» باشد، بعد «Patch Engineer»، بعد «Validation Auditor»، و فقط در آخر شاید «Trading Co-pilot».

## کارهای مجاز

- خواندن repo و Obsidian.
- ساخت hypothesis و experiment template.
- بررسی contradiction.
- ساخت report و validation checklist.
- پیشنهاد patch و commit message.
- تحلیل ژورنال و ساخت label.

## کارهای غیرمجاز در MVP

- live order.
- افزایش risk.
- override کردن rule engine.
- merge خودکار patch.
- تأیید نتیجه بدون baseline.

## معماری پیشنهادی

```text
User
→ Alpha Lab Orchestrator
→ Librarian / Research / Patch / Validation / Journal Agents
→ Tools: Git, Obsidian, Python, MQL5, Registry
→ Human/Rule Engine Approval
```
