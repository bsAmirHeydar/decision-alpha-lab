import argparse,json
from .catalog import build_default_catalog
from .conformance import run_catalog_conformance
def main(argv=None):
 p=argparse.ArgumentParser(prog='strategy-factory-treatments-v3'); s=p.add_subparsers(dest='cmd',required=True)
 s.add_parser('catalog'); s.add_parser('conformance')
 a=p.parse_args(argv)
 if a.cmd=='catalog':
  c=build_default_catalog(); print(json.dumps({'atom_count':c.atom_count,'registries':{r.kind.value:[x.descriptor.exact_key for x in r.all()] for r in c.registries()}},indent=2,sort_keys=True))
 else: print(json.dumps(run_catalog_conformance().to_dict(),indent=2,sort_keys=True))
 return 0
if __name__=='__main__': raise SystemExit(main())
