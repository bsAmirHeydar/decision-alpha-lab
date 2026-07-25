# Phoenix Level 18 Static QA

Level 18 is the compile/static QA hardening layer after the official Level 17 decision lock.

Run from repository root:

```powershell
python contexts/legacy/tools/flag_counting/static_qa.py --root . --csv reports/flag_counting_static_qa.csv
```

Strict mode fails on warnings too:

```powershell
python contexts/legacy/tools/flag_counting/static_qa.py --root . --strict
```

The scanner checks Phoenix MQL files for:

- empty `Print()` calls
- very long multi-argument `Print(...)` calls
- duplicate EA input names
- stale `phoenix_level16` / `phoenix_level17` identity pass references in MQL source
- stale interface contract versions
- stale short report aliases such as `r.export_forced`
- missing Level 18 modules

The MQL runtime layer prints `FP_LEVEL18`; this Python scanner is the source-side companion for checks that cannot be proven from inside MQL5 at runtime.
