from __future__ import annotations
from .cube import build_cube
from .integrity import build_receipt

def replay(*args,expected_cube_hash:str,**kwargs):
    cube=build_cube(*args,**kwargs);match=cube.cube_hash==expected_cube_hash
    return cube,{'expected_cube_hash':expected_cube_hash,'observed_cube_hash':cube.cube_hash,'match':match,'integrity_receipt':build_receipt(cube)}
