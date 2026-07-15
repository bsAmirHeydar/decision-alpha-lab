from __future__ import annotations
import argparse,json
from pathlib import Path
from .serialization import load_json,dump_json
from .service import build_reference_bundle

def main(argv=None):
    p=argparse.ArgumentParser(prog='saed-v4-11')
    sub=p.add_subparsers(dest='command',required=True)
    b=sub.add_parser('build-reference-bundle');b.add_argument('--records',required=True);b.add_argument('--upstream-manifest',required=True);b.add_argument('--handoff',required=True);b.add_argument('--config',required=True);b.add_argument('--split-policy',required=True);b.add_argument('--canaries',required=True);b.add_argument('--output-dir',required=True)
    a=p.parse_args(argv)
    if a.command=='build-reference-bundle':
        canary_doc=load_json(a.canaries);bundle,streams=build_reference_bundle(load_json(a.records),load_json(a.upstream_manifest),load_json(a.handoff),load_json(a.config),load_json(a.split_policy),canary_doc['tokens'])
        out=Path(a.output_dir);out.mkdir(parents=True,exist_ok=True)
        for name,obj in bundle.items():dump_json(out/(name.upper()+'.JSON'),obj)
        dump_json(out/'TOKEN_STREAMS.JSON',{"phase":"SAED_V4_11","streams":streams})
        print(json.dumps({"passed":True,"artifact_count":len(bundle)+1,"output_dir":str(out)},sort_keys=True))
        return 0
    return 2
if __name__=='__main__': raise SystemExit(main())
