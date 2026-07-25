from __future__ import annotations
import argparse,json
from pathlib import Path
from .exporter import LinearScalarParameters,export_to_file,inspect_linear_scalar_onnx

def main(argv=None):
    parser=argparse.ArgumentParser(prog="strategy-factory-inference")
    sub=parser.add_subparsers(dest="command",required=True)
    export=sub.add_parser("export-linear"); export.add_argument("--weights",required=True); export.add_argument("--bias",type=float,required=True); export.add_argument("--out",required=True)
    inspect=sub.add_parser("inspect"); inspect.add_argument("model")
    args=parser.parse_args(argv)
    if args.command=="export-linear": result=export_to_file(LinearScalarParameters(tuple(float(x) for x in args.weights.split(',')),args.bias),args.out)
    else: result=inspect_linear_scalar_onnx(Path(args.model).read_bytes())
    print(json.dumps(result,indent=2,sort_keys=True)); return 0
if __name__=="__main__": raise SystemExit(main())
