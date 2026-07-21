# EXP0017 Chapter 08 Patch — Candle-Close Confirmation Doctrine

This patch adds the Chapter 08 strategy-architect answer layer for EXP0017 Cycle Group Intermarket Divergence.

## Scope

Chapter 08 documents the strategic doctrine around:

- candle-close confirmation,
- the distinction between hunt occurrence and signal permission,
- divergence invalidation when both symbols hunt the reference,
- temporal close-only confirmation,
- keeping all confirmed divergences visible and valid,
- allowing trade permission after confirmation.

No trading-engine code is included in this patch.
No previous chapter doctrine is removed.
No previous expert implementation is modified.

## Install

From the repository root:

```powershell
Expand-Archive -Force ".\decision-alpha-lab-exp0017-chapter08-close-confirmation-expanded-obsidian-patch.zip" ".\"
Remove-Item ".\decision-alpha-lab-exp0017-chapter08-close-confirmation-expanded-obsidian-patch.zip"
```
