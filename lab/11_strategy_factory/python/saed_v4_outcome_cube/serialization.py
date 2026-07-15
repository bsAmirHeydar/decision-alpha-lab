from __future__ import annotations
import json

def cube_to_dict(cube):return dict(cube.semantic_payload(),cube_id=cube.cube_id,cube_hash=cube.cube_hash)
def dumps(cube):return json.dumps(cube_to_dict(cube),indent=2,sort_keys=True,ensure_ascii=False)+'\n'
