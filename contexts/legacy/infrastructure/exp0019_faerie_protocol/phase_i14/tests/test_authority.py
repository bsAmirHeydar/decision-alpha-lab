from pathlib import Path
from fp_i14_diagnostic import *
def test_python_authority_clean():
    root=Path(__file__).resolve().parents[1]/'python/fp_i14_diagnostic'
    paths=[p for p in root.glob('*.py') if p.name not in {'constants.py','authority.py'}]
    assert scan_forbidden(paths)==()
def test_runtime_authority_registry(): assert registry()['runtime_authority']=='NONE'
