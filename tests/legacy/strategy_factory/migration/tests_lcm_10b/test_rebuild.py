from pathlib import Path
from src.engine.tooling.strategy_factory.lcm.lcm_10b.service import LCM10BTreatmentBoundaryService
from src.engine.tooling.strategy_factory.lcm.lcm_10b.canonical import file_digest
from .conftest import REPO,ROOT
def test_rebuild_is_byte_deterministic(tmp_path:Path):
 out=tmp_path/"package";LCM10BTreatmentBoundaryService().build(REPO,out);a={p.relative_to(ROOT).as_posix():file_digest(p) for p in ROOT.rglob("*") if p.is_file()};b={p.relative_to(out).as_posix():file_digest(p) for p in out.rglob("*") if p.is_file()};assert a==b
