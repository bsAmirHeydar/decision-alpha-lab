#ifndef __UCEI12_CATALOG_MQH__
#define __UCEI12_CATALOG_MQH__

#include "UCEI12_SuiteDescriptor.mqh"

class CUCEI12Catalog
  {
private:
   static void Fill(UCEI12_SuiteDescriptor &out,const string key,const bool critical,const bool seed_required,const string inputs,const string outputs)
     {
      out.key=key; out.version="1.0.0"; out.critical=critical; out.deterministic=true;
      out.seed_required=seed_required; out.required_inputs=inputs; out.outputs=outputs;
     }
public:
   static int Count() { return 7; }
   static bool Get(const int index,UCEI12_SuiteDescriptor &out)
     {
      switch(index)
        {
         case 0: Fill(out,"uce.promotion.uncertainty",true,true,"returns,dependence_identity","uncertainty_report"); return true;
         case 1: Fill(out,"uce.promotion.multiplicity",true,false,"selection_universe,family_definition","multiplicity_report"); return true;
         case 2: Fill(out,"uce.promotion.winner_overfit",true,true,"performance_matrix,trial_universe","pbo,deflation,reality_check,spa"); return true;
         case 3: Fill(out,"uce.promotion.null_controls",true,true,"observed,null_plan","null_results"); return true;
         case 4: Fill(out,"uce.promotion.stress",true,true,"returns,stress_plan","stress_results"); return true;
         case 5: Fill(out,"uce.promotion.calibration",false,false,"oof_probabilities,labels","calibration_report"); return true;
         case 6: Fill(out,"uce.promotion.scorecard",true,false,"all_evidence,policy","promotion_decision"); return true;
        }
      return false;
     }
  };

#endif
