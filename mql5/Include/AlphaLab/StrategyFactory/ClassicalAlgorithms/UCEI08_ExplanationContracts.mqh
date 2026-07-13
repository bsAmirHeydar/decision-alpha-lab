#ifndef UCEI08_EXPLANATION_CONTRACTS_MQH
#define UCEI08_EXPLANATION_CONTRACTS_MQH
struct UCEI08_FeatureImportance{string feature_name;int feature_index;string kind;double mean_importance;double std_importance;double direction;string fold_id;string role;string model_state_hash;int rank;};
struct UCEI08_ExplanationManifest{string explanation_id;string request_id;string algorithm_key;string dataset_manifest_hash;string fold_id;string role;bool selection_safe;string evidence_hash;string limitations_csv;};
bool UCEI08_ExplanationSelectionAllowed(const string role,const bool for_selection){return !(role=="final_test" && for_selection);}
#endif
