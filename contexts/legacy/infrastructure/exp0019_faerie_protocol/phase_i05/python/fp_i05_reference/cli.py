import json
from .conformance import run_conformance
def main(argv=None):
    report=run_conformance();print(json.dumps(report,indent=2,sort_keys=True));return 0 if report['passed'] else 1
if __name__=='__main__':raise SystemExit(main())
