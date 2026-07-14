from __future__ import annotations
import argparse, json
from pathlib import Path
from .compiler import compile_twin
from .contracts import load_document

def main(argv=None):
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest='cmd', required=True)
    compile_cmd = sub.add_parser('compile')
    compile_cmd.add_argument('--context-spec', required=True)
    compile_cmd.add_argument('--seed', required=True)
    compile_cmd.add_argument('--output')
    args = parser.parse_args(argv)
    if args.cmd == 'compile':
        manifest = compile_twin(load_document(args.context_spec), load_document(args.seed))
        output = {**manifest.semantic_payload(), 'semantic_hash': manifest.semantic_hash}
        text = json.dumps(output, indent=2, sort_keys=True)
        if args.output:
            Path(args.output).write_text(text + '\n', encoding='utf-8')
        else:
            print(text)
        return 0
    return 2

if __name__ == '__main__':
    raise SystemExit(main())
