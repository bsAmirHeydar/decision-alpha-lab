from pathlib import Path
import argparse
import json
from .service import run_reference

def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))

def main(argv=None):
    parser=argparse.ArgumentParser()
    parser.add_argument('--config',required=True)
    parser.add_argument('--upstream',required=True)
    parser.add_argument('--score-table',required=True)
    parser.add_argument('--output',required=True)
    args=parser.parse_args(argv)
    out=run_reference(load(args.config),load(args.upstream),load(args.score_table))
    Path(args.output).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8',newline='\n')
    return 0

if __name__=='__main__':
    raise SystemExit(main())
