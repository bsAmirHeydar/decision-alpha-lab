#ifndef __SF13_PREDICTION_RECORD_MQH__
#define __SF13_PREDICTION_RECORD_MQH__
#include "SF13_ModelArtifact.mqh"
struct SF13_PredictionRecord{string model_artifact_hash;string calibration_hash;string dataset_hash;string row_id;string fold_id;ENUM_SF13_PREDICTION_ROLE role;double raw_score;double probability;double action_score;long generated_at_utc_msc;string prediction_id;string prediction_hash;};
string SF13_PredictionIdentity(const SF13_PredictionRecord &v){return v.model_artifact_hash+"|"+v.dataset_hash+"|"+v.row_id+"|"+v.fold_id+"|"+IntegerToString((int)v.role);}
string SF13_DerivePredictionId(const SF13_PredictionRecord &v){return SF01_StableId("pred",SF13_PredictionIdentity(v));}
string SF13_PredictionCanonical(const SF13_PredictionRecord &v){return "alpha_lab.strategy_factory/prediction_record@1.0.0|"+v.prediction_id+"|"+SF13_PredictionIdentity(v)+"|"+v.calibration_hash+"|"+SF01_CanonicalDouble(v.raw_score,10)+"|"+SF01_CanonicalDouble(v.probability,10)+"|"+SF01_CanonicalDouble(v.action_score,10)+"|"+IntegerToString(v.generated_at_utc_msc);}
string SF13_DerivePredictionHash(const SF13_PredictionRecord &v){return SF01_StableId("predh",SF13_PredictionCanonical(v));}
bool SF13_ValidatePrediction(const SF13_PredictionRecord &v,string &error){if(v.model_artifact_hash==""||v.calibration_hash==""||v.dataset_hash==""||v.row_id==""||v.fold_id==""||v.role!=SF13_PREDICTION_TEST_OOS||!MathIsValidNumber(v.raw_score)||!MathIsValidNumber(v.probability)||v.probability<0||v.probability>1){error="prediction is not valid test OOS evidence";return false;}if(v.prediction_id!=""&&v.prediction_id!=SF13_DerivePredictionId(v)){error="prediction id mismatch";return false;}if(v.prediction_hash!=""&&v.prediction_hash!=SF13_DerivePredictionHash(v)){error="prediction hash mismatch";return false;}error="";return true;}
#endif
