from __future__ import annotations
import json,subprocess,sys
from pathlib import Path
from .policies import REPO_ROOT

def run()->dict:
    commands=[['pytest','-q','lab/11_strategy_factory/acl_os/tests_acl_06'],[sys.executable,'-m','compileall','-q','tools/strategy_factory/acl_os/acl_06'],[sys.executable,'-m','tools.strategy_factory.acl_os.acl_06.validate_acl_06'],[sys.executable,'-m','tools.strategy_factory.acl_os.acl_06.validate_acl_06_delivery']]
    results=[]
    for cmd in commands:
        p=subprocess.run(cmd,cwd=REPO_ROOT,text=True,capture_output=True); results.append({'command':' '.join(cmd),'returncode':p.returncode,'stdout':p.stdout[-4000:],'stderr':p.stderr[-2000:]})
    out={'phase':'ACL-06','checks':results,'passed':all(x['returncode']==0 for x in results)}; print(json.dumps(out,indent=2,sort_keys=True)); return out
if __name__=='__main__': raise SystemExit(0 if run()['passed'] else 2)
