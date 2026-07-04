# DATA-R02 — Label and Event Ledger

## Purpose
چون اگر eventها و labelها دقیق ذخیره نشوند، بعداً train/test ممکن نیست. AI باید بداند چه چیزی ساخته، بسته، باطل، missed، fill یا completed شده است.

## Required Clarifications
- چه زمانی node_created ثبت شود؟
- CycleHook born/dead چطور ثبت شود؟
- Sequence closed و X/Y closed چطور label شوند؟
- Zone promoted و zone destroyed چطور ثبت شوند؟
- Scenario born/updated/repriced/dead چطور ثبت شوند؟
- Entry extreme created/invalidated چطور ثبت شود؟
- Limit created/canceled/missed/replaced/filled چطور ثبت شود؟
- Destination consumed/completed چطور ثبت شود؟
- Position partially exited/fully exited چطور ثبت شود؟
- Outcome metrics هر event چه باشد؟

## Image Requirement
خیر. پاسخ متنی کافی است.

## Expected Derived Outputs
- `nds_event_ledger_v1.csv`
- `training_label_taxonomy_v1.csv`
- `scenario_outcome_ledger_v1.csv`
- `entry_outcome_ledger_v1.csv`
