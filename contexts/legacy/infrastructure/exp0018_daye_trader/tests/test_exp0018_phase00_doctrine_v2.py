from tools.repository_paths import find_repository_root
import csv, json, unittest
from pathlib import Path
ROOT=find_repository_root(__file__)
BASE=ROOT/'docs/operations/execution/EXP0018_daye_trader_intermarket_divergence/implementation_design_v2/07_phase00_doctrine_freeze_v2'
class Phase00DoctrineTests(unittest.TestCase):
    def test_decisions_and_adrs(self):
        with open(BASE/'data/EXP0018_PHASE00_DECISION_LEDGER_V2.csv',encoding='utf-8-sig',newline='') as f:
            rows=list(csv.DictReader(f))
        self.assertEqual(12,len(rows)); self.assertEqual(12,len({r['decision_id'] for r in rows}))
        self.assertEqual(12,len(list((BASE/'adr').glob('ADR-DY-A*.md'))))
    def test_relationship_count(self):
        with open(BASE/'data/EXP0018_PHASE00_RELATIONSHIP_SNAPSHOT_V2.csv',encoding='utf-8-sig',newline='') as f:
            rows=list(csv.DictReader(f))
        self.assertEqual(22,len(rows)); self.assertEqual(6,sum(int(r['major']) for r in rows)); self.assertEqual(16,sum(1-int(r['major']) for r in rows))
    def test_no_execution_authority(self):
        snap=json.loads((BASE/'data/EXP0018_PHASE00_DOCTRINE_SNAPSHOT_V2.json').read_text(encoding='utf-8'))
        self.assertFalse(snap['execution_authority'])
    def test_critical_fixture_coverage(self):
        with open(BASE/'data/EXP0018_PHASE00_FIXTURE_REGISTRY_V2.csv',encoding='utf-8-sig',newline='') as f:
            rows=list(csv.DictReader(f))
        covered={r['rule_or_decision'] for r in rows}
        for did in ['DY-A01','DY-A02','DY-A03','DY-A04','DY-A05','DY-A12']: self.assertIn(did,covered)
if __name__=='__main__': unittest.main()
