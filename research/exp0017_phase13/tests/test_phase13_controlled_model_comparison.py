import csv, json, subprocess, sys, tempfile, unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "python" / "phase13_controlled_model_comparison.py"

class Phase13SmokeTest(unittest.TestCase):
    def test_synthetic_walk_forward(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); out = root / "out"
            fields = ["sample_id","signal_id","model_use_status","confirmation_ny","primary_r","label_binary_win","group","group_minutes","current_cycle","reference_cycle","reference_age_cycles","direction","direction_code","side","side_code","clean_symbol","hunter_symbol","role_key","hour_ny","minute_of_day_ny","session_ny","stop_points"]
            with (root / "EXP0017_Phase10_Model_Dataset.csv").open("w", newline="", encoding="utf-8") as f:
                w = csv.DictWriter(f, fieldnames=fields); w.writeheader()
                for i in range(240):
                    day = i + 1
                    import datetime as dt
                    t = dt.datetime(2025,1,1) + dt.timedelta(days=day)
                    direction = "BUY" if i % 2 == 0 else "SELL"
                    role = "SPX_hunter__NDX_clean" if i % 3 else "NDX_hunter__SPX_clean"
                    r = (0.8 if direction == "BUY" else -0.25) + (0.3 if role.startswith("SPX") else -0.1) + ((i % 7)-3)*0.05
                    w.writerow({"sample_id":f"S{i}","signal_id":f"G{i}","model_use_status":"model_ready","confirmation_ny":t.strftime("%Y.%m.%d %H:%M:%S"),"primary_r":r,"label_binary_win":1 if r>0 else 0,"group":"cg_30m" if i%2==0 else "cg_60m","group_minutes":30 if i%2==0 else 60,"current_cycle":5,"reference_cycle":3,"reference_age_cycles":2,"direction":direction,"direction_code":1 if direction=="BUY" else -1,"side":"LOW" if direction=="BUY" else "HIGH","side_code":1 if direction=="BUY" else -1,"clean_symbol":"NDX" if role.startswith("SPX") else "SPX","hunter_symbol":"SPX" if role.startswith("SPX") else "NDX","role_key":role,"hour_ny":10+(i%6),"minute_of_day_ny":600+(i%360),"session_ny":"CASH","stop_points":100+(i%30)})
            fold_fields = ["fold_id","train_start","train_end","embargo_start","embargo_end","test_start","test_end","train_count","test_count","usable","status"]
            with (root / "EXP0017_Phase11_Fold_Plan.csv").open("w", newline="", encoding="utf-8") as f:
                w=csv.DictWriter(f,fieldnames=fold_fields);w.writeheader()
                import datetime as dt
                base=dt.datetime(2025,1,1)
                for fold_id, start in enumerate((0,40,80),1):
                    tr0=base+dt.timedelta(days=start+1); tr1=base+dt.timedelta(days=start+120)
                    em0=tr1; em1=tr1+dt.timedelta(days=1); te0=em1; te1=te0+dt.timedelta(days=30)
                    w.writerow({"fold_id":fold_id,"train_start":tr0.strftime("%Y.%m.%d %H:%M:%S"),"train_end":tr1.strftime("%Y.%m.%d %H:%M:%S"),"embargo_start":em0.strftime("%Y.%m.%d %H:%M:%S"),"embargo_end":em1.strftime("%Y.%m.%d %H:%M:%S"),"test_start":te0.strftime("%Y.%m.%d %H:%M:%S"),"test_end":te1.strftime("%Y.%m.%d %H:%M:%S"),"train_count":120,"test_count":30,"usable":1,"status":"usable"})
            integrity = root / "integrity.json"; integrity.write_text(json.dumps({"status":"READY_FOR_PHASE13"}), encoding="utf-8")
            result = subprocess.run([sys.executable,str(SCRIPT),"--data-dir",str(root),"--out-dir",str(out),"--integrity-summary",str(integrity),"--min-train-rows","50","--min-test-rows","10","--min-bucket-rows","10","--min-threshold-side-rows","10","--logistic-epochs","8","--ridge-epochs","8"], text=True, capture_output=True)
            self.assertEqual(result.returncode,0,msg=result.stderr+result.stdout)
            self.assertTrue((out/"phase13_experiment_leaderboard.csv").exists())
            summary=json.loads((out/"phase13_comparison_summary.json").read_text())
            self.assertGreaterEqual(summary["folds_used"],2)
            self.assertFalse(summary["execution_authority"])

if __name__ == "__main__": unittest.main()
