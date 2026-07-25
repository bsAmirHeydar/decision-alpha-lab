from __future__ import annotations
import json
from .registry import FeatureRegistry
from .fixtures import fixture_nodes

def main()->int:
    registry=FeatureRegistry()
    for node in fixture_nodes():registry.register(node)
    print(json.dumps({'order':registry.compile(),'graph_hash':registry.graph_hash},indent=2));return 0
if __name__=='__main__':raise SystemExit(main())
