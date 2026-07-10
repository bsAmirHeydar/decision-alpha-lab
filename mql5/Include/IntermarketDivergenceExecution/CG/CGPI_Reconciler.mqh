//+------------------------------------------------------------------+
//| CGPI_Reconciler.mqh                                              |
//| Phase 12.5 — Cross-phase lineage, metrics, and readiness gates   |
//+------------------------------------------------------------------+
#property strict
#ifndef __CGPI_RECONCILER_MQH__
#define __CGPI_RECONCILER_MQH__

#include <IntermarketDivergenceExecution/CG/CGPI_Types.mqh>
#include <IntermarketDivergenceExecution/CG/CGPI_CsvInspector.mqh>

class CCGPI_Reconciler
{
private:
   CCGPI_CsvInspector m_inspector;

   void AddRecon(SCGPIReconciliationRow &rows[],const SCGPIReconciliationRow &row)
   {
      int n=ArraySize(rows); ArrayResize(rows,n+1); rows[n]=row;
   }

   void AddMetric(SCGPIMetricCheck &rows[],const string name,const string lf,const string lm,const double lv,
                  const string rf,const string rm,const double rv,const double tolerance,const string notes)
   {
      int n=ArraySize(rows); ArrayResize(rows,n+1);
      rows[n].check_name=name; rows[n].left_file=lf; rows[n].left_metric=lm; rows[n].left_value=lv;
      rows[n].right_file=rf; rows[n].right_metric=rm; rows[n].right_value=rv;
      rows[n].delta=lv-rv; rows[n].tolerance=tolerance;
      rows[n].status=(MathAbs(rows[n].delta)<=tolerance ? "PASS" : "FAIL");
      rows[n].notes=notes;
   }

   void AddGate(SCGPIReadinessGate &gates[],const string name,const bool required,const bool passed,
                const ECGPISeverity severity,const string evidence,const string remediation)
   {
      int n=ArraySize(gates); ArrayResize(gates,n+1);
      gates[n].gate_name=name; gates[n].required=required; gates[n].passed=passed;
      gates[n].severity=severity; gates[n].evidence=evidence; gates[n].remediation=remediation;
   }

   int FindAudit(SCGPIFileAuditRow &audits[],const string logical_name)
   {
      for(int i=0;i<ArraySize(audits);i++) if(audits[i].logical_name==logical_name) return i;
      return -1;
   }

public:
   void Setup(const bool common_files) { m_inspector.Setup(common_files); }

   bool ReconcileKeys(const string relation_name,const ECGPIRelationMode mode,
                      const string parent_file,const string parent_key,
                      const string child_file,const string child_key,
                      const SCGPIConfig &cfg,SCGPIReconciliationRow &rows[],string &diagnostics[])
   {
      string parent[]; string child[];
      int pr=0,pe=0,pd=0,cr=0,ce=0,cd=0;
      string pdiag="",cdiag="";
      bool pok=m_inspector.LoadUniqueKeys(parent_file,parent_key,cfg.max_keys_to_reconcile,parent,pr,pe,pd,pdiag);
      bool cok=m_inspector.LoadUniqueKeys(child_file,child_key,cfg.max_keys_to_reconcile,child,cr,ce,cd,cdiag);
      if(!pok) CGPI_AddDiagnostic(diagnostics,relation_name+":"+pdiag);
      if(!cok) CGPI_AddDiagnostic(diagnostics,relation_name+":"+cdiag);

      SCGPIReconciliationRow row;
      row.relation_name=relation_name; row.relation_mode=mode;
      row.parent_file=parent_file; row.parent_key=parent_key;
      row.child_file=child_file; row.child_key=child_key;
      row.parent_unique_keys=ArraySize(parent); row.child_unique_keys=ArraySize(child);
      row.matched_keys=0; row.missing_in_child=0; row.orphan_in_child=0;
      row.parent_coverage_percent=0.0; row.child_coverage_percent=0.0;
      row.status="FAILED_TO_LOAD"; row.notes="";

      if(!pok || !cok) { AddRecon(rows,row); return false; }

      int i=0,j=0;
      while(i<ArraySize(parent) && j<ArraySize(child))
      {
         int cmp=StringCompare(parent[i],child[j],true);
         if(cmp==0) { row.matched_keys++; i++; j++; }
         else if(cmp<0) { row.missing_in_child++; i++; }
         else { row.orphan_in_child++; j++; }
      }
      row.missing_in_child += ArraySize(parent)-i;
      row.orphan_in_child += ArraySize(child)-j;
      row.parent_coverage_percent=CGPI_SafePercent(row.matched_keys,ArraySize(parent));
      row.child_coverage_percent=CGPI_SafePercent(row.matched_keys,ArraySize(child));

      bool pass=false;
      if(mode==CGPI_RELATION_EXACT)
         pass=(row.parent_coverage_percent>=cfg.minimum_exact_lineage_coverage_percent && row.orphan_in_child==0);
      else
         pass=(row.orphan_in_child==0 && (ArraySize(child)==0 || row.child_coverage_percent>=99.999));
      row.status=pass ? "PASS" : "FAIL";
      row.notes="parent_empty="+IntegerToString(pe)+";parent_duplicates="+IntegerToString(pd)+
                ";child_empty="+IntegerToString(ce)+";child_duplicates="+IntegerToString(cd)+";";
      AddRecon(rows,row);
      return pass;
   }

   void BuildMetricChecks(const SCGPIConfig &cfg,SCGPIFileAuditRow &audits[],SCGPIMetricCheck &rows[],string &diagnostics[])
   {
      ArrayResize(rows,0);
      int p10=FindAudit(audits,"model_dataset");
      int p11fp=FindAudit(audits,"fold_plan");
      int p11pred=FindAudit(audits,"predictions");
      int p11bucket=FindAudit(audits,"bucket_validation");

      string diag=""; double v=0.0;
      if(p10>=0 && m_inspector.ReadMetricValue(cfg.phase10_label_summary_file,"rows_written",v,diag))
         AddMetric(rows,"phase10_summary_vs_dataset",cfg.phase10_label_summary_file,"rows_written",v,
                   cfg.phase10_dataset_file,"data_rows",audits[p10].row_count,cfg.allowed_count_difference,
                   "Dataset row count must equal the Phase10 writer summary.");
      else if(StringLen(diag)>0) CGPI_AddDiagnostic(diagnostics,diag);

      diag=""; v=0.0;
      if(p11fp>=0 && m_inspector.ReadMetricValue(cfg.phase11_experiment_summary_file,"folds_built",v,diag))
         AddMetric(rows,"phase11_summary_vs_fold_plan",cfg.phase11_experiment_summary_file,"folds_built",v,
                   cfg.phase11_fold_plan_file,"data_rows",audits[p11fp].row_count,cfg.allowed_count_difference,
                   "Fold plan must reconcile to folds_built.");
      else if(StringLen(diag)>0) CGPI_AddDiagnostic(diagnostics,diag);

      diag=""; v=0.0;
      if(p11pred>=0 && m_inspector.ReadMetricValue(cfg.phase11_experiment_summary_file,"predictions_written",v,diag))
         AddMetric(rows,"phase11_summary_vs_predictions",cfg.phase11_experiment_summary_file,"predictions_written",v,
                   cfg.phase11_predictions_file,"data_rows",audits[p11pred].row_count,cfg.allowed_count_difference,
                   "Prediction file row count must reconcile to summary.");
      else if(StringLen(diag)>0) CGPI_AddDiagnostic(diagnostics,diag);

      diag=""; v=0.0;
      if(p11bucket>=0 && m_inspector.ReadMetricValue(cfg.phase11_experiment_summary_file,"bucket_models_built",v,diag))
         AddMetric(rows,"phase11_summary_vs_bucket_validation",cfg.phase11_experiment_summary_file,"bucket_models_built",v,
                   cfg.phase11_bucket_validation_file,"data_rows",audits[p11bucket].row_count,cfg.allowed_count_difference,
                   "Bucket validation rows must reconcile to bucket_models_built.");
      else if(StringLen(diag)>0) CGPI_AddDiagnostic(diagnostics,diag);

      int complete=m_inspector.CountRowsWhere(cfg.phase07_outcome_file,"availability","COMPLETE",diag);
      double overall=0.0; string diag2="";
      if(complete>=0 && m_inspector.ReadFirstNumericColumnValue(cfg.phase08_overall_file,"sample_count",overall,diag2))
         AddMetric(rows,"phase07_complete_vs_phase08_overall",cfg.phase07_outcome_file,"COMPLETE_rows",complete,
                   cfg.phase08_overall_file,"sample_count",overall,cfg.allowed_count_difference,
                   "Phase08 overall sample count should equal COMPLETE Phase07 outcomes.");
      else
      {
         if(StringLen(diag)>0) CGPI_AddDiagnostic(diagnostics,diag);
         if(StringLen(diag2)>0) CGPI_AddDiagnostic(diagnostics,diag2);
      }
   }

   void BuildReadinessGates(const SCGPIConfig &cfg,SCGPIFileAuditRow &audits[],SCGPISchemaIssue &issues[],
                            SCGPIReconciliationRow &recons[],SCGPIMetricCheck &metrics[],
                            SCGPIReadinessGate &gates[],SCGPIRunStats &stats)
   {
      ArrayResize(gates,0);
      int missing_required=0,failed_files=0,duplicates=0,empty_keys=0,ts_failures=0;
      for(int i=0;i<ArraySize(audits);i++)
      {
         if(audits[i].required && !audits[i].exists) missing_required++;
         if(audits[i].status=="FAILED" || audits[i].status=="OPEN_FAILED" || audits[i].status=="EMPTY_FILE") failed_files++;
         duplicates+=audits[i].duplicate_primary_keys;
         empty_keys+=audits[i].empty_primary_keys;
         ts_failures+=audits[i].timestamp_parse_failures;
      }
      int critical_issues=0;
      for(int i=0;i<ArraySize(issues);i++) if(issues[i].severity==CGPI_SEVERITY_CRITICAL) critical_issues++;
      int lineage_failures=0;
      for(int i=0;i<ArraySize(recons);i++) if(recons[i].status!="PASS") lineage_failures++;
      int metric_failures=0;
      for(int i=0;i<ArraySize(metrics);i++) if(metrics[i].status!="PASS") metric_failures++;

      AddGate(gates,"critical_files_present",true,missing_required==0,CGPI_SEVERITY_CRITICAL,
              "missing_required="+IntegerToString(missing_required),"Run the missing upstream phase and regenerate its output file.");
      AddGate(gates,"required_schema_complete",true,critical_issues==0 && failed_files==0,CGPI_SEVERITY_CRITICAL,
              "critical_issues="+IntegerToString(critical_issues)+";failed_files="+IntegerToString(failed_files),
              "Align CSV headers with the Phase12.5 schema contract before model comparison.");
      AddGate(gates,"primary_keys_unique_and_present",true,duplicates==0 && empty_keys==0,CGPI_SEVERITY_CRITICAL,
              "duplicates="+IntegerToString(duplicates)+";empty_keys="+IntegerToString(empty_keys),
              "Fix signal/sample identity generation or duplicate writer behavior.");
      AddGate(gates,"cross_phase_lineage_reconciled",true,lineage_failures==0,CGPI_SEVERITY_CRITICAL,
              "failed_relations="+IntegerToString(lineage_failures),
              "Regenerate downstream files from the same upstream dataset and inspect orphan/missing keys.");
      AddGate(gates,"writer_metrics_reconciled",true,metric_failures==0,CGPI_SEVERITY_ERROR,
              "failed_metric_checks="+IntegerToString(metric_failures),
              "Re-run the affected phase and compare writer summaries with actual CSV row counts.");
      AddGate(gates,"timestamps_parseable",true,ts_failures==0,CGPI_SEVERITY_ERROR,
              "timestamp_parse_failures="+IntegerToString(ts_failures),
              "Normalize all research timestamps to the documented MQL datetime representation.");
      AddGate(gates,"minimum_research_population",false,
              FindAudit(audits,"model_dataset")>=0 && audits[FindAudit(audits,"model_dataset")].row_count>0,
              CGPI_SEVERITY_WARNING,"phase10_rows="+(FindAudit(audits,"model_dataset")>=0 ? IntegerToString(audits[FindAudit(audits,"model_dataset")].row_count) : "0"),
              "Generate Phase10 rows before beginning controlled model comparison.");

      stats.readiness_gates=ArraySize(gates); stats.readiness_failures=0;
      bool critical_failure=false; bool any_failure=false;
      for(int i=0;i<ArraySize(gates);i++)
      {
         if(!gates[i].passed)
         {
            stats.readiness_failures++; any_failure=true;
            if(gates[i].severity==CGPI_SEVERITY_CRITICAL && gates[i].required) critical_failure=true;
         }
      }
      if(critical_failure && cfg.block_phase13_on_critical_failure) stats.readiness_status="BLOCKED_FOR_PHASE13";
      else if(any_failure) stats.readiness_status="READY_WITH_WARNINGS";
      else stats.readiness_status="READY_FOR_PHASE13";
   }
};

#endif
//+------------------------------------------------------------------+
