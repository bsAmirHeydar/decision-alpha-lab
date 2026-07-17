#ifndef DAL_SAED_V426_ACTIVATION_PATCHING_MQH
#define DAL_SAED_V426_ACTIVATION_PATCHING_MQH
bool SAEDV426PatchEligible(const string model_a,const string model_b,const datetime source_time,const datetime decision_time){ return model_a==model_b && source_time<=decision_time; }
#endif
