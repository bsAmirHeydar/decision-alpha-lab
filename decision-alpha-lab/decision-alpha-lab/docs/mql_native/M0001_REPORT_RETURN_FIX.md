# M0001 Report Return Fix

## Fix

`DAL_WriteM0001ExcelReport()` returns `bool`, but the success path at the end of
the function was missing `return true`.

MetaEditor error:

```text
'}' - not all control paths return a value
DAL_ValidationJournal.mqh
```

## Version

`M0001_LiveVisualLab.mq5` version: `1.37`.
