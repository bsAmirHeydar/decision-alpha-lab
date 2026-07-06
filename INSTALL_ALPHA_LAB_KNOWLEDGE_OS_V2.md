
# نصب Alpha Lab Knowledge OS V2

این patch را داخل ریشه پروژه expand کن. چون تو قبلاً patch قبلی را expand کرده‌ای، این نسخه روی مسیر جدید `docs/obsidian_deep` می‌نشیند و با قبلی conflict اصلی ندارد.

## PowerShell

```powershell
Expand-Archive -Path .lpha_lab_obsidian_deep_design_patch.zip -DestinationPath . -Force
Remove-Item .lpha_lab_obsidian_deep_design_patch.zip
```

## باز کردن در Obsidian

1. Obsidian را باز کن.
2. `Open folder as vault` را بزن.
3. ریشه پروژه را انتخاب کن.
4. فایل زیر را باز کن:

```text
00_ALPHA_LAB_KNOWLEDGE_OS.md
```

## فایل‌های اصلی

- `00_ALPHA_LAB_KNOWLEDGE_OS.md`
- `docs/obsidian_deep/00_master_command_center.md`
- `docs/obsidian_deep/01_canonical_model/README.md`
- `docs/obsidian_deep/04_relationships/traceability_matrix.md`
- `docs/obsidian_deep/07_canvases/full_system_architecture.canvas`
