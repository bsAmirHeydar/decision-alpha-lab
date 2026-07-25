from pathlib import Path
from fp_i13_release.authority import scan_paths
def test_python_package_has_no_authority():
 p=Path(__file__).resolve().parents[1]/'python/fp_i13_release';assert scan_paths([p])==()
