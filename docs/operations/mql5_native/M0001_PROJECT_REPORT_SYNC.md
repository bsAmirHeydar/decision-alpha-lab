# M0001 Project Report Sync

## Why

MQL5 file writing is sandboxed. The expert cannot reliably write directly into the
repository working tree from Strategy Tester.

So the expert now writes reports to a project-relative path inside the MT5 file
sandbox:

```text
reports\mql_native\M0001\
```

Then the sync script copies the generated files into the same folder inside this
repository:

```text
reports/mql_native/M0001/
```

## Expert inputs

```text
InpWriteExcelReport = true
InpExcelReportUseFullHistorySnapshot = true
InpJournalPrefix = reports\mql_native\M0001\
```

CSV journals still use the same prefix.

## Sync command

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\sync_m0001_reports_to_project.ps1 -TerminalDataPath "<MT5 terminal data path>"
```

If you do not know the exact tester agent folder, the script also searches under:

```text
%APPDATA%\MetaQuotes
```

## Output files

```text
reports/mql_native/M0001/<symbol>_M0001_full_audit_report.xls
reports/mql_native/M0001/<symbol>_M0001_nodes.csv
reports/mql_native/M0001/<symbol>_M0001_node_audit_states.csv
reports/mql_native/M0001/<symbol>_M0001_events.csv
```

## Version

`M0001_LiveVisualLab.mq5` version: `1.35`.
