#ifndef __UCEI10_REGIME_FUSION_CONTRACTS_MQH__
#define __UCEI10_REGIME_FUSION_CONTRACTS_MQH__

#include "UCEI10_Enums.mqh"

struct UCEI10_RegimeNoveltyPrediction
  {
   string                       prediction_id;
   string                       row_id;
   string                       regime_id;
   double                       regime_probability;
   double                       novelty_score;
   double                       change_score;
   int                          support_count;
   UCEI10_REGIME_GATE_DECISION decision;
   string                       expert_key;
   string                       reason;
   string                       evidence_hash;

   bool Valid() const
     {
      return prediction_id!="" && row_id!="" && regime_id!="" &&
             MathIsValidNumber(regime_probability) &&
             regime_probability>=0.0 && regime_probability<=1.0 &&
             MathIsValidNumber(novelty_score) &&
             MathIsValidNumber(change_score) && support_count>=0 &&
             reason!="" && evidence_hash!="";
     }
  };

struct UCEI10_FusionPrediction
  {
   string                    prediction_id;
   string                    row_id;
   UCEI10_FUSION_KIND        fusion_kind;
   UCEI10_MISSING_VIEW_POLICY missing_policy;
   int                       available_view_count;
   int                       missing_view_count;
   double                    weight_sum;
   double                    value;
   double                    uncertainty;
   bool                      abstained;
   string                    reason;
   string                    evidence_hash;

   bool Valid() const
     {
      if(prediction_id=="" || row_id=="" || reason=="" || evidence_hash=="")
         return false;
      if(available_view_count<0 || missing_view_count<0)
         return false;
      if(!MathIsValidNumber(value) || !MathIsValidNumber(uncertainty) || uncertainty<0.0)
         return false;
      if(!abstained && MathAbs(weight_sum-1.0)>1e-9)
         return false;
      return true;
     }
  };

#endif
