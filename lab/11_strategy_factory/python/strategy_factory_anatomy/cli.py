from __future__ import annotations
import argparse
from pathlib import Path
from .golden import load_manifest,verify_fixture
def main()->int:
    p=argparse.ArgumentParser();p.add_argument('manifest');p.add_argument('fixture');a=p.parse_args();m=load_manifest(Path(a.manifest));verify_fixture(m,Path(a.fixture));print('SF06 golden ledger: PASS');return 0
if __name__=='__main__':raise SystemExit(main())
