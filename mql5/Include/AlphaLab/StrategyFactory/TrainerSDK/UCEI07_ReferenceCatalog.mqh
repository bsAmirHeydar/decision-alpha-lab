#ifndef ALPHALAB_UCEI07_REFERENCE_CATALOG_MQH
#define ALPHALAB_UCEI07_REFERENCE_CATALOG_MQH
#include "UCEI07_TrainerRegistry.mqh"
class CUCEI07ReferenceCatalog{
private:
 UCEI07_TrainerCapability Make(const string id,const string family,const string tasks,const string views,const string targets,const long outputs){UCEI07_TrainerCapability c;c.trainer_id=id;c.trainer_version="1.0.0";c.family=family;c.supported_tasks=tasks;c.supported_views=views;c.supported_target_shapes=targets;c.supported_tensors="dense_float64";c.missingness_support="reject";c.calibration_kinds="none|identity";c.explainability_kinds="global_parameters";c.export_formats="native_json";c.devices="cpu";c.precisions="float64";c.determinism=UCEI07_DETERMINISM_BIT_EXACT;c.sample_weight=true;c.multi_output=(outputs>1);c.warm_start=false;c.checkpoint=false;c.cancel=true;c.min_rows=1;c.max_features=100000;c.max_outputs=outputs;c.descriptor_hash=UCEI07_StableId("ucedesc",id+"@1.0.0|"+tasks+"|"+views);return c;}
public:
 bool RegisterAll(CUCEI07TrainerRegistry &r,string &reason){UCEI07_TrainerCapability a=Make("uce.reference.prior_binary","reference_baseline",IntegerToString((long)UCEI07_TASK_BINARY),IntegerToString((long)UCEI07_VIEW_TABULAR),"scalar_binary",1);if(!r.Register(a,reason))return false;UCEI07_TrainerCapability b=Make("uce.reference.mean_regression","reference_baseline",IntegerToString((long)UCEI07_TASK_REGRESSION),IntegerToString((long)UCEI07_VIEW_TABULAR),"scalar_continuous",1);if(!r.Register(b,reason))return false;UCEI07_TrainerCapability c=Make("uce.reference.linear_ranker","reference_baseline",IntegerToString((long)UCEI07_TASK_RANKING),IntegerToString((long)UCEI07_VIEW_TABULAR),"listwise",1);if(!r.Register(c,reason))return false;r.Freeze();return true;}
};
#endif
