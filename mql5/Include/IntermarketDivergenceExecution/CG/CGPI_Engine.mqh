//+------------------------------------------------------------------+
//| CGPI_Engine.mqh                                                  |
//| Phase 12.5 — Full integrity-audit orchestration                  |
//+------------------------------------------------------------------+
#property strict
#ifndef __CGPI_ENGINE_MQH__
#define __CGPI_ENGINE_MQH__

#include <IntermarketDivergenceExecution/CG/CGPI_Types.mqh>
#include <IntermarketDivergenceExecution/CG/CGPI_Contracts.mqh>
#include <IntermarketDivergenceExecution/CG/CGPI_CsvInspector.mqh>
#include <IntermarketDivergenceExecution/CG/CGPI_Reconciler.mqh>
#include <IntermarketDivergenceExecution/CG/CGPI_Ledger.mqh>
#include <IntermarketDivergenceExecution/CG/CGPI_Display.mqh>

class CCGPI_Engine
{
private:
   CCGPI_Contracts    m_contracts;
   CCGPI_CsvInspector m_inspector;
   CCGPI_Reconciler   m_reconciler;
   CCGPI_Ledger       m_ledger;
   CCGPI_Display      m_display;

   string Out(const SCGPIConfig &cfg,const string suffix) { return cfg.output_prefix+"_"+suffix; }

   void AggregateStats(SCGPIFileContract &contracts[],SCGPIFileAuditRow &audits[],SCGPISchemaIssue &issues[],
                       SCGPIReconciliationRow &recons[],SCGPIMetricCheck &metrics[],SCGPIRunStats &s)
   {
      s.contracts_total=ArraySize(contracts); s.required_files=0; s.files_found=0; s.files_missing=0;
      s.schema_issues=ArraySize(issues); s.critical_schema_issues=0;
      s.duplicate_primary_keys=0; s.empty_primary_keys=0;
      for(int i=0;i<ArraySize(contracts);i++) if(contracts[i].required) s.required_files++;
      for(int i=0;i<ArraySize(audits);i++)
      {
         if(audits[i].exists) s.files_found++; else s.files_missing++;
         s.duplicate_primary_keys+=audits[i].duplicate_primary_keys;
         s.empty_primary_keys+=audits[i].empty_primary_keys;
      }
      for(int i=0;i<ArraySize(issues);i++) if(issues[i].severity==CGPI_SEVERITY_CRITICAL) s.critical_schema_issues++;
      s.lineage_checks=ArraySize(recons); s.lineage_failures=0;
      for(int i=0;i<ArraySize(recons);i++) if(recons[i].status!="PASS") s.lineage_failures++;
      s.metric_checks=ArraySize(metrics); s.metric_failures=0;
      for(int i=0;i<ArraySize(metrics);i++) if(metrics[i].status!="PASS") s.metric_failures++;
   }

public:
   bool Run(const SCGPIConfig &cfg)
   {
      SCGPIRunStats stats;
      stats.contracts_total=0; stats.required_files=0; stats.files_found=0; stats.files_missing=0;
      stats.schema_issues=0; stats.critical_schema_issues=0; stats.duplicate_primary_keys=0; stats.empty_primary_keys=0;
      stats.lineage_checks=0; stats.lineage_failures=0; stats.metric_checks=0; stats.metric_failures=0;
      stats.readiness_gates=0; stats.readiness_failures=0; stats.readiness_status="STARTED"; stats.message="";
      string diagnostics[];

      m_inspector.Setup(cfg.use_common_files);
      m_reconciler.Setup(cfg.use_common_files);
      m_ledger.Setup(cfg.use_common_files);

      SCGPIFileContract contracts[];
      m_contracts.Build(cfg,contracts);
      SCGPIFileAuditRow audits[];
      SCGPISchemaIssue issues[];
      ArrayResize(audits,ArraySize(contracts));
      for(int i=0;i<ArraySize(contracts);i++)
         m_inspector.Inspect(contracts[i],cfg,audits[i],issues,diagnostics);

      SCGPIReconciliationRow recons[];
      if(cfg.enable_lineage_reconciliation)
      {
         m_reconciler.ReconcileKeys("phase07_outcome_to_phase10_outcome",CGPI_RELATION_EXACT,
            cfg.phase07_outcome_file,"outcome_id",cfg.phase10_dataset_file,"outcome_id",cfg,recons,diagnostics);
         m_reconciler.ReconcileKeys("phase07_signal_to_phase10_signal",CGPI_RELATION_EXACT,
            cfg.phase07_outcome_file,"signal_id",cfg.phase10_dataset_file,"signal_id",cfg,recons,diagnostics);
         m_reconciler.ReconcileKeys("phase10_sample_to_phase11_prediction",CGPI_RELATION_CHILD_SUBSET,
            cfg.phase10_dataset_file,"sample_id",cfg.phase11_predictions_file,"sample_id",cfg,recons,diagnostics);
         m_reconciler.ReconcileKeys("phase10_signal_to_phase11_prediction",CGPI_RELATION_CHILD_SUBSET,
            cfg.phase10_dataset_file,"signal_id",cfg.phase11_predictions_file,"signal_id",cfg,recons,diagnostics);
         m_reconciler.ReconcileKeys("phase11_fold_plan_to_predictions",CGPI_RELATION_CHILD_SUBSET,
            cfg.phase11_fold_plan_file,"fold_id",cfg.phase11_predictions_file,"fold_id",cfg,recons,diagnostics);
      }

      SCGPIMetricCheck metrics[];
      if(cfg.enable_metric_reconciliation)
         m_reconciler.BuildMetricChecks(cfg,audits,metrics,diagnostics);

      AggregateStats(contracts,audits,issues,recons,metrics,stats);
      SCGPIReadinessGate gates[];
      m_reconciler.BuildReadinessGates(cfg,audits,issues,recons,metrics,gates,stats);
      stats.message=(stats.readiness_status=="READY_FOR_PHASE13" ? "pipeline_contracts_reconciled" : "review_integrity_outputs_before_phase13");

      if(cfg.write_file_audit) m_ledger.WriteFileAudit(Out(cfg,"File_Audit.csv"),cfg.clear_outputs_on_run,audits);
      if(cfg.write_schema_issues) m_ledger.WriteSchemaIssues(Out(cfg,"Schema_Issues.csv"),cfg.clear_outputs_on_run,issues);
      if(cfg.write_key_reconciliation) m_ledger.WriteReconciliation(Out(cfg,"Key_Reconciliation.csv"),cfg.clear_outputs_on_run,recons);
      if(cfg.write_metric_reconciliation) m_ledger.WriteMetrics(Out(cfg,"Metric_Reconciliation.csv"),cfg.clear_outputs_on_run,metrics);
      if(cfg.write_readiness_gates) m_ledger.WriteGates(Out(cfg,"Readiness_Gates.csv"),cfg.clear_outputs_on_run,gates);
      if(cfg.write_readiness_summary) m_ledger.WriteSummary(Out(cfg,"Readiness_Summary.csv"),cfg.clear_outputs_on_run,stats);
      if(cfg.write_diagnostics) m_ledger.WriteDiagnostics(Out(cfg,"Diagnostics.csv"),cfg.clear_outputs_on_run,diagnostics);

      m_display.Show(cfg,stats);
      m_display.PrintSummary(cfg,stats);
      return stats.readiness_status!="BLOCKED_FOR_PHASE13";
   }
};

#endif
//+------------------------------------------------------------------+
