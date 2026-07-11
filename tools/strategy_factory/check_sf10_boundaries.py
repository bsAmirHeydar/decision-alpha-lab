from pathlib import Path
import sys,re
root=Path(sys.argv[1] if len(sys.argv)>1 else ".").resolve();targets=list((root/"mql5").rglob("SF10_*.*"))
errors=[]
for p in targets:
 t=p.read_text(encoding="utf-8",errors="ignore")
 for bad in ("OrderSend(","OrderCheck(","CTrade","LongToString"):
  if bad in t: errors.append(f"{p.relative_to(root)}: forbidden token {bad}")
 if "CopyRates(" in t or "SymbolInfoTick(" in t: errors.append(f"{p.relative_to(root)}: market access bypasses shared services")
print(f"SF10 boundary files={len(targets)} errors={len(errors)}")
for e in errors:print(e)
raise SystemExit(1 if errors else 0)
