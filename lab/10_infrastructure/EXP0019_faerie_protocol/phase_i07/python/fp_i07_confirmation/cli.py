import json
from dataclasses import asdict
from .conformance import run_conformance
from .registry import validate_registry
def main():
    validate_registry();print(json.dumps({"phase":"FP-I07","conformance":run_conformance()},indent=2))
if __name__=="__main__":main()
