# M0001 Reports

This folder is the project-side destination for M0001 generated reports.

MetaTrader cannot write directly into the repository working tree because MQL file
I/O is sandboxed. The expert writes reports inside the terminal/tester `MQL5\Files`
sandbox using this relative path:

```text
reports\mql_native\M0001\
```

Use:

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\sync_m0001_reports_to_project.ps1 -TerminalDataPath "<MT5 terminal data path>"
```

to copy the generated reports into this project folder.
