from pathlib import Path
import subprocess,sys,json
ROOT=Path(__file__).resolve().parents[3]
cmds=[('python_tests',[sys.executable,'tools/strategy_factory/saed_v4_21/run_saed_v4_21_tests.py']),('contracts',[sys.executable,'tools/strategy_factory/saed_v4_21/validate_saed_v4_21_contracts.py']),('status',[sys.executable,'tools/strategy_factory/saed_v4_21/validate_saed_v4_21_status.py']),('boundaries',[sys.executable,'tools/strategy_factory/saed_v4_21/check_saed_v4_21_boundaries.py']),('obsidian',[sys.executable,'tools/strategy_factory/saed_v4_21/validate_saed_v4_21_obsidian.py']),('mql5_static',[sys.executable,'tools/strategy_factory/saed_v4_21/validate_saed_v4_21_mql5_static.py']),('golden_reproduction',[sys.executable,'tools/strategy_factory/saed_v4_21/reproduce_saed_v4_21_golden.py'])]
out={'phase':'SAED_V4_21','passed':True,'checks':{}}
for name,cmd in cmds:
 r=subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True)
 if r.returncode:
  print(r.stdout);print(r.stderr,file=sys.stderr);raise SystemExit(r.returncode)
 lines=[x for x in r.stdout.splitlines() if x.strip()];data={}
 for line in reversed(lines):
  try:data=json.loads(line);break
  except Exception:pass
 out['checks'][name]=data
out['python_tests']=out['checks']['python_tests'].get('python_tests',0);out['closed_schema_pairs']=out['checks']['contracts'].get('closed_schema_pairs',0);out['obsidian_notes']=out['checks']['obsidian'].get('obsidian_notes',0);out['mql5_static_files']=out['checks']['mql5_static'].get('mql5_static_files',0);out['metaeditor_compile']='pending_local_windows';out['external_evidence_attached']=False
print(json.dumps(out,sort_keys=True))
