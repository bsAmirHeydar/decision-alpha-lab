import json
from .conformance import run_conformance

def main():
    print(json.dumps(run_conformance(),indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
