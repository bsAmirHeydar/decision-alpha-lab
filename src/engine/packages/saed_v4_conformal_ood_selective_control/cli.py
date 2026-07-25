from pathlib import Path
import argparse
import json
from .service import run

def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', required=True)
    parser.add_argument('--upstream', required=True)
    parser.add_argument('--records', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args(argv)
    load = lambda path: json.loads(Path(path).read_text(encoding='utf-8'))
    output = run(load(args.config), load(args.upstream), load(args.records))
    Path(args.output).write_text(json.dumps(output, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
