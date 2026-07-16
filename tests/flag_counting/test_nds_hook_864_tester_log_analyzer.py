from __future__ import annotations
import importlib.util
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[2]
PATH=ROOT/'tools/flag_counting/analyze_nds_hook_864_tester_log.py'
spec=importlib.util.spec_from_file_location('nds_hook_864_log',PATH)
assert spec and spec.loader
m=importlib.util.module_from_spec(spec); sys.modules[spec.name]=m; spec.loader.exec_module(m)


class TesterLogAnalyzerTests(unittest.TestCase):
    def test_detects_wrong_profile(self):
        result=m.analyze_text('NDS_BT_INIT status=ready runtime_profile=FAST trade_profile=TERMINAL_F123 orders=enabled')
        codes={item['code'] for item in result['findings']}
        self.assertIn('wrong_trade_profile',codes)
        self.assertIn('sparse_runtime_profile',codes)

    def test_reports_structural_blocker(self):
        text='''NDS_BT_INIT status=ready runtime_profile=PARITY trade_profile=HOOK_864_CYCLE_R1 orders=enabled
NDS_BT profile=PARITY ok=true status=NO_ELIGIBLE_HOOK_864_CYCLE_R1_SETUP reason=x funnel={total=9;canonical=8;family=4;allowed=4;confirmed=4;crown=4;x34=0;mature=0;p04=0;closed=0;alive=0;untouched=0;ready=0;blocker=no_x3_or_x4_sequence}
NDS_BT_SESSION runs=100 ready_runs=0 paper_ready=0 limits_sent=0 blocked=0'''
        result=m.analyze_text(text)
        self.assertEqual(result['funnel']['blocker'],'no_x3_or_x4_sequence')
        self.assertTrue(any(x['code']=='no_x3_or_x4_sequence' for x in result['findings']))

    def test_ready_but_not_sent_is_downstream(self):
        text='''NDS_BT_INIT status=ready runtime_profile=PARITY trade_profile=HOOK_864_CYCLE_R1 orders=enabled
NDS_BT profile=PARITY ok=true status=BLOCKED reason=broker funnel={total=2;canonical=2;family=2;allowed=2;confirmed=2;crown=2;x34=1;mature=1;p04=1;closed=1;alive=1;untouched=1;ready=1;blocker=ready_candidate_exists}
NDS_BT_SESSION runs=10 ready_runs=1 paper_ready=0 limits_sent=0 blocked=1'''
        result=m.analyze_text(text)
        codes={item['code'] for item in result['findings']}
        self.assertIn('ready_candidate_exists',codes)
        self.assertIn('ready_but_not_sent',codes)

    def test_missing_init_is_explicit(self):
        result=m.analyze_text('unrelated log')
        self.assertEqual(result['findings'][0]['code'],'init_missing')


if __name__=='__main__': unittest.main()
