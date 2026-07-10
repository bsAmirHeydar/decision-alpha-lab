---
id: EXP0018-P02-SYMBOL-MAPPING
title: "P02 Symbol Mapping Contract"
type: contract
status: active
project: EXP0018
---
# قرارداد نگاشت نماد

- `InpSymbolA/B` نام واقعی بروکر هستند.
- `InpCanonicalSymbolA/B` شناسه پایدار پژوهشی هستند.
- suffix یا prefix بروکر خودکار حدس زده نمی‌شود.
- symbolها باید متمایز باشند.
- `SymbolExist`, `SymbolSelect`, `SYMBOL_SELECT`, `SYMBOL_DIGITS` و `SYMBOL_POINT` بررسی می‌شوند.
- failure در انتخاب symbol باعث Init failure می‌شود؛ چون config اشتباه است، نه داده موقت.

تغییر broker symbol نباید هویت canonical historical dataset را تغییر دهد.
