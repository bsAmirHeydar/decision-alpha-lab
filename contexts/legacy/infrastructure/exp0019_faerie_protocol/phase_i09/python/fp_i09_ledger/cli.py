import json
from .conformance import run_conformance
if __name__=="__main__": print(json.dumps(run_conformance(),indent=2,sort_keys=True))
