from __future__ import annotations
import json,subprocess,sys,tempfile
from pathlib import Path
from .policies import REPO_ROOT
from .replay import verify_research_run

def run()->dict:
    root=REPO_ROOT/'src/engine/legacy/acl_os_reference/fixtures/acl_06/reference_run'; replay=verify_research_run(root)
    result={'phase':'ACL-06','reference_replay':replay,'passed':replay['passed']}; print(json.dumps(result,indent=2,sort_keys=True)); return result
if __name__=='__main__': raise SystemExit(0 if run()['passed'] else 2)
