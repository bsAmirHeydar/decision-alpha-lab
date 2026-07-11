#ifndef __SF12_VALIDATION_ENGINE_MQH__
#define __SF12_VALIDATION_ENGINE_MQH__
#include "SF12_ValidationGate.mqh"
#include "SF12_ValidationTelemetry.mqh"
class CSF12ValidationEngine
{
private:
   SF12_FoldObservation m_rows[];SF12_ValidationTelemetry m_telemetry;
   bool AddGate(SF12_PromotionDecision &d,const SF12_GateResult &g)
   {const int n=ArraySize(d.gates);ArrayResize(d.gates,n+1);d.gates[n]=g;m_telemetry.gates_evaluated++;if(g.status==SF12_GATE_FAIL)m_telemetry.gates_failed++;return true;}
   void AddReason(string &reasons,const SF12_GateResult &g) const{if(g.status!=SF12_GATE_FAIL)return;if(reasons!="")reasons+=";";reasons+=g.reason_code;}
public:
   CSF12ValidationEngine(){Reset();}
   void Reset(void){ArrayResize(m_rows,0);ZeroMemory(m_telemetry);}
   bool Observe(const SF12_FoldObservation &input,string &error)
   {
      SF12_FoldObservation row=input;if(!SF12_ValidateFoldObservation(row,error)){m_telemetry.observations_rejected++;return false;}
      if(row.observation_hash=="")row.observation_hash=SF12_DeriveFoldObservationHash(row);if(row.ambiguous){m_telemetry.ambiguous_excluded++;error="";return true;}
      for(int i=0;i<ArraySize(m_rows);i++)if(m_rows[i].observation_id==row.observation_id){error="duplicate fold observation";m_telemetry.observations_rejected++;return false;}
      const int n=ArraySize(m_rows);ArrayResize(m_rows,n+1);m_rows[n]=row;m_telemetry.observations_accepted++;error="";return true;
   }
   bool Finalize(const string decision_id,const string plan_hash,const string trial_id,const SF12_PromotionThresholds &t,const SF12_ExternalDiagnostics &x,SF12_PromotionDecision &d,string &error)
   {
      const ulong start=GetMicrosecondCount();double is_total=0.0,oos_total=0.0,best=-DBL_MAX,worst_fold=DBL_MAX;long is_n=0,oos_n=0;string fold_ids[];double fold_sum[];long fold_count[];
      for(int i=0;i<ArraySize(m_rows);i++){const SF12_FoldObservation r=m_rows[i];if(r.trial_id!=trial_id)continue;if(r.role==SF12_ROLE_TRAIN){is_total+=r.net_r;is_n++;}
         if(r.role==SF12_ROLE_TEST){oos_total+=r.net_r;oos_n++;if(r.net_r>best)best=r.net_r;int idx=-1;for(int k=0;k<ArraySize(fold_ids);k++)if(fold_ids[k]==r.fold_id){idx=k;break;}
            if(idx<0){idx=ArraySize(fold_ids);ArrayResize(fold_ids,idx+1);ArrayResize(fold_sum,idx+1);ArrayResize(fold_count,idx+1);fold_ids[idx]=r.fold_id;fold_sum[idx]=0.0;fold_count[idx]=0;}
            fold_sum[idx]+=r.net_r;fold_count[idx]++;}}
      if(oos_n==0||is_n==0){error="missing train or test observations";return false;}int positive=0;for(int i=0;i<ArraySize(fold_ids);i++){const double mean=fold_sum[i]/(double)MathMax(1,fold_count[i]);if(mean>0.0)positive++;if(mean<worst_fold)worst_fold=mean;}
      m_telemetry.folds_seen=ArraySize(fold_ids);const double is_mean=is_total/(double)is_n;const double oos_mean=oos_total/(double)oos_n;const double positive_share=(ArraySize(fold_ids)>0)?(double)positive/(double)ArraySize(fold_ids):0.0;
      const double ratio=(is_mean>0.0)?oos_mean/is_mean:0.0;const double best_removed=(oos_n>1)?(oos_total-best)/(double)(oos_n-1):0.0;
      d.schema="alpha_lab.strategy_factory/promotion_decision@1.0.0";d.decision_id=decision_id;d.plan_hash=plan_hash;d.selected_trial_id=trial_id;d.status=SF12_PROMOTION_ELIGIBLE_FOR_DATASET_REVIEW;ArrayResize(d.gates,0);d.rejection_reasons="";d.evidence_hashes=x.diagnostics_hash;d.decision_hash="";
      SF12_GateResult g;
      g=SF12_MakeGate("minimum_oos_folds",ArraySize(fold_ids)>=t.minimum_oos_folds,(double)ArraySize(fold_ids),(double)t.minimum_oos_folds,">=","INSUFFICIENT_OOS_FOLDS");AddGate(d,g);AddReason(d.rejection_reasons,g);
      g=SF12_MakeGate("minimum_oos_samples",oos_n>=t.minimum_oos_samples,(double)oos_n,(double)t.minimum_oos_samples,">=","INSUFFICIENT_OOS_SAMPLES");AddGate(d,g);AddReason(d.rejection_reasons,g);
      g=SF12_MakeGate("positive_fold_share",positive_share>=t.minimum_positive_fold_share,positive_share,t.minimum_positive_fold_share,">=","FOLD_SIGN_INSTABILITY");AddGate(d,g);AddReason(d.rejection_reasons,g);
      g=SF12_MakeGate("worst_fold",worst_fold>=t.minimum_worst_fold_mean_r,worst_fold,t.minimum_worst_fold_mean_r,">=","WORST_FOLD_FAILURE");AddGate(d,g);AddReason(d.rejection_reasons,g);
      g=SF12_MakeGate("oos_to_is_ratio",ratio>=t.minimum_oos_to_is_ratio,ratio,t.minimum_oos_to_is_ratio,">=","EXCESSIVE_IS_OOS_DECAY");AddGate(d,g);AddReason(d.rejection_reasons,g);
      g=SF12_MakeGate("pbo",x.probability_of_backtest_overfitting<=t.maximum_pbo,x.probability_of_backtest_overfitting,t.maximum_pbo,"<=","PBO_TOO_HIGH");AddGate(d,g);AddReason(d.rejection_reasons,g);
      g=SF12_MakeGate("deflated_probability",x.deflated_probability>=t.minimum_deflated_probability,x.deflated_probability,t.minimum_deflated_probability,">=","DEFLATED_PERFORMANCE_WEAK");AddGate(d,g);AddReason(d.rejection_reasons,g);
      g=SF12_MakeGate("reality_check",x.reality_check_p<=t.maximum_reality_check_p,x.reality_check_p,t.maximum_reality_check_p,"<=","REALITY_CHECK_NOT_SIGNIFICANT");AddGate(d,g);AddReason(d.rejection_reasons,g);
      g=SF12_MakeGate("surface_support",x.surface_support>=t.minimum_surface_support,x.surface_support,t.minimum_surface_support,">=","PARAMETER_ISLAND");AddGate(d,g);AddReason(d.rejection_reasons,g);
      g=SF12_MakeGate("best_trade_removal",best_removed>=t.minimum_best_trade_removed_mean_r,best_removed,t.minimum_best_trade_removed_mean_r,">=","BEST_TRADE_DEPENDENCY");AddGate(d,g);AddReason(d.rejection_reasons,g);
      g=SF12_MakeGate("stress_floor",x.stress_floor_mean_r>=t.minimum_stress_floor_mean_r,x.stress_floor_mean_r,t.minimum_stress_floor_mean_r,">=","STRESS_FRAGILITY");AddGate(d,g);AddReason(d.rejection_reasons,g);
      if(d.rejection_reasons!="")d.status=SF12_PROMOTION_REJECTED;d.decision_hash=SF01_StableId("prom",d.schema+"|"+d.decision_id+"|"+d.plan_hash+"|"+d.selected_trial_id+"|"+IntegerToString((int)d.status)+"|"+d.rejection_reasons+"|"+d.evidence_hashes);
      m_telemetry.last_finalize_microseconds=(long)(GetMicrosecondCount()-start);if(m_telemetry.last_finalize_microseconds>m_telemetry.maximum_finalize_microseconds)m_telemetry.maximum_finalize_microseconds=m_telemetry.last_finalize_microseconds;error="";return true;
   }
   SF12_ValidationTelemetry Telemetry(void) const{return m_telemetry;}
};
#endif
