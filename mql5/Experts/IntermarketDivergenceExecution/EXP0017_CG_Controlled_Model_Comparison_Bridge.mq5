//+------------------------------------------------------------------+
//| EXP0017_CG_Controlled_Model_Comparison_Bridge.mq5                |
//| Phase 13 — MQL5 preflight bridge for Python model comparison     |
//+------------------------------------------------------------------+
#property strict
#property version   "13.00"
#property description "Research-only Phase 13 bridge. No trading or strategy mutation."

#include <IntermarketDivergenceExecution/CG/CGP13_Engine.mqh>

input string InpPhase10DatasetFile        = "EXP0017_Phase10_Model_Dataset.csv";
input string InpPhase11FoldPlanFile       = "EXP0017_Phase11_Fold_Plan.csv";
input string InpPhase125ReadinessFile     = "EXP0017_Phase12_5_Readiness_Summary.csv";
input string InpOutputPrefix              = "EXP0017_Phase13";
input string InpPythonScript              = "research/exp0017_phase13/python/phase13_controlled_model_comparison.py";
input string InpPythonOutputDir           = "research/exp0017_phase13/outputs";
input int    InpDeterministicSeed         = 170013;
input bool   InpRequireIntegrityGate      = true;
input bool   InpAllowReadyWithWarnings    = true;
input bool   InpShowChartComment          = false;
input bool   InpPrintSummary              = true;
input bool   InpRemoveExpertAfterRun      = true;

CCGP13_Engine g_phase13;

int OnInit()
{
   SCGP13Config cfg;
   cfg.phase10_dataset_file=InpPhase10DatasetFile;
   cfg.phase11_fold_plan_file=InpPhase11FoldPlanFile;
   cfg.phase12_5_readiness_file=InpPhase125ReadinessFile;
   cfg.output_prefix=InpOutputPrefix;
   cfg.python_script=InpPythonScript;
   cfg.python_output_dir=InpPythonOutputDir;
   cfg.deterministic_seed=InpDeterministicSeed;
   cfg.require_integrity_gate=InpRequireIntegrityGate;
   cfg.allow_ready_with_warnings=InpAllowReadyWithWarnings;
   cfg.show_chart_comment=InpShowChartComment;
   cfg.print_summary=InpPrintSummary;

   SCGP13Summary summary;
   bool ok=g_phase13.Run(cfg,summary);
   if(InpRemoveExpertAfterRun) ExpertRemove();
   return ok ? INIT_SUCCEEDED : INIT_FAILED;
}

void OnTick() {}
void OnDeinit(const int reason) { if(!InpShowChartComment) Comment(""); }
