# INSTALL — EXP0017 CG Intermarket Divergence Docs Patch

این patch فقط داکیومنت و آبسیدین EXP0017 را اضافه می‌کند. هیچ فایل MQL5 فعلی را تغییر نمی‌دهد و هیچ اکسپرت موجودی را دست‌کاری نمی‌کند.

## PowerShell install

از ریشه پروژه اجرا کن:

```powershell
Expand-Archive -Force ".\decision-alpha-lab-exp0017-cg-intermarket-divergence-docs-patch.zip" ".\"
Remove-Item ".\decision-alpha-lab-exp0017-cg-intermarket-divergence-docs-patch.zip"
```

## Added paths

```text
docs/execution/EXP0017_cycle_group_intermarket_divergence/
lab/09_execution/EXP0017_cycle_group_intermarket_divergence/
docs/obsidian/02_mocs/cg_intermarket_divergence_moc.md
docs/obsidian_deep/00_mocs/CG_INTERMARKET_DIVERGENCE_MOC.md
docs/obsidian_deep/01_concepts/
docs/obsidian_deep/02_architecture/
docs/obsidian_deep/04_checklists/
```

## Scope

- Strategy documentation
- Cycle group doctrine
- Divergence rules
- Input contract
- Drawing contract
- Execution/risk contract
- MQL5 modular architecture plan
- Test plan
- Obsidian knowledge notes

## Not included

- No MQL5 implementation yet
- No changes to existing EXP0015 / EXP0016 files
- No dependency on STC/W-cycle expert
- No astrology, NDS, Flag, Hook logic
