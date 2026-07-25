from __future__ import annotations
import json
from .fixtures import build_fixture_registry,build_reference_matrix

def main():
    r=build_fixture_registry();m=build_reference_matrix(r)
    print(json.dumps({"registry_hash":r.registry_hash,"matrix_hash":m.plan_hash,"templates":len(m.templates)},indent=2))
if __name__=="__main__":main()
