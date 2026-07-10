---
id: EXP0018-P02-ROLLBACK
title: "P02 Rollback Plan"
type: rollback
status: active
project: EXP0018
---
# Rollback

برای rollback، Expert و includeهای `DAYE_Data*` را حذف یا commit پچ را revert کن. P01 untouched باقی می‌ماند. Audit CSVها source code نیستند و باید جداگانه archive یا حذف شوند.

Rollback نباید Phase01 time kernel را حذف کند.
