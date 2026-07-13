import argparse,json
from .conformance import run_conformance
def main(argv=None):
    p=argparse.ArgumentParser(prog="fp-i08");p.add_argument("command",choices=["conformance"]);a=p.parse_args(argv)
    if a.command=="conformance": print(json.dumps(run_conformance(),indent=2));return 0
if __name__=="__main__": raise SystemExit(main())
