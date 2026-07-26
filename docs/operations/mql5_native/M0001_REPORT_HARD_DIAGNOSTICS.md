# M0001 Report Hard Diagnostics

## Fix

Report generation now has hard diagnostics and fallback behavior.

## Inputs

```text
InpWriteExcelReport = true
InpExcelReportUseFullHistorySnapshot = true
InpWriteReportProbe = true
InpJournalPrefix = reports\mql_native\M0001\
```

## What happens on init

If `InpWriteExcelReport=true`, the expert immediately writes probe files:

```text
<symbol>_M0001_REPORT_PROBE.txt
reports\mql_native\M0001\<symbol>_M0001_REPORT_PROBE.txt
```

If these files are not created, the EA is not running with report writing enabled,
the compiled version is not the new one, or MT5 file I/O is failing.

## Experts log messages

The expert prints:

```text
DAL M0001 report env | context=...
DAL probe written: ...
DAL Excel report open ok: ...
DAL Excel report open failed: ... err=...
DAL Excel report fallback open ok: ...
DAL M0001 Excel report written: ...
```

## Fallback

If writing to the project-relative sandbox path fails:

```text
reports\mql_native\M0001\<symbol>_M0001_full_audit_report.xls
```

the writer falls back to the root MT5 Files sandbox:

```text
<symbol>_M0001_full_audit_report.xls
```

## Version

`M0001_LiveVisualLab.mq5` version: `1.36`.
