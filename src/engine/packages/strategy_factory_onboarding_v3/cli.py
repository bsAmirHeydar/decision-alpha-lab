from __future__ import annotations
import argparse,json
from pathlib import Path
from .golden import golden_run
def main(argv=None)->int:
    p=argparse.ArgumentParser();p.add_argument('--repo-root',default='.');p.add_argument('--output');a=p.parse_args(argv)
    run=golden_run(Path(a.repo_root));payload={'context_spec_hash':run[0].spec_hash,'manifest_hash':run[2].manifest_hash,'compiled_tournament_hash':run[4].compiled_hash,'invariance':run[5].status.value,'parity':run[7].status.value,'migration_report_hash':run[9].report_hash}
    text=json.dumps(payload,sort_keys=True,separators=(',',':'))
    if a.output:Path(a.output).write_text(text,encoding='utf-8')
    else:print(text)
    return 0
if __name__=='__main__':raise SystemExit(main())
