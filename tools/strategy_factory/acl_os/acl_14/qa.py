from __future__ import annotations
import subprocess,sys,os
from pathlib import Path
from .delivery_validation import validate_delivery
from .static_validation import validate_registry
def run(root:Path)->dict:
    commands=[[sys.executable,'-m','compileall','-q',str(root/'tools/strategy_factory/acl_os/acl_14')],[sys.executable,'-m','pytest','-q',str(root/'lab/11_strategy_factory/acl_os/tests_acl_14')],[sys.executable,'-m','pytest','-q',str(root/'lab/11_strategy_factory/acl_os/tests_acl_13')]]
    results=[]
    for cmd in commands:
        p=subprocess.run(cmd,cwd=root,text=True,capture_output=True,env={**os.environ,'PYTEST_DISABLE_PLUGIN_AUTOLOAD':'1'}); results.append({'command':' '.join(cmd),'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr})
    static=validate_registry(root); delivery=validate_delivery(root)
    return {'passed':all(x['returncode']==0 for x in results) and static['passed'] and delivery['passed'],'commands':results,'static':static,'delivery':delivery}
