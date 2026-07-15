from pathlib import Path
import subprocess,sys,json,time
ROOT=Path(__file__).resolve().parents[3];commands=[['python','tools/strategy_factory/saed_v4_10/validate_saed_v4_10_contracts.py'],['python','tools/strategy_factory/saed_v4_10/check_saed_v4_10_boundaries.py'],['python','tools/strategy_factory/saed_v4_10/validate_saed_v4_10_mql5_static.py'],['python','tools/strategy_factory/saed_v4_10/validate_saed_v4_10_obsidian.py'],['python','tools/strategy_factory/saed_v4_10/run_saed_v4_10_tests.py']];results=[]
for c in commands:
 s=time.time();r=subprocess.run(c,cwd=ROOT,text=True,capture_output=True);results.append({'command':' '.join(c),'returncode':r.returncode,'seconds':round(time.time()-s,3),'stdout':r.stdout[-4000:],'stderr':r.stderr[-4000:]});print(r.stdout,end='');print(r.stderr,end='',file=sys.stderr)
 if r.returncode:break
report={'phase':'SAED_V4_10','passed':all(x['returncode']==0 for x in results) and len(results)==len(commands),'results':results,'external_evidence':{'metaeditor_compile':'pending_local_windows','prospective_paper':'not_claimed','shadow':'not_claimed','live':'not_claimed'}};(ROOT/'SAED_V4_10_QA_REPORT.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n');raise SystemExit(0 if report['passed'] else 1)
