#ifndef ALPHALAB_OPERATIONS_CHANGE_GUARD_MQH
#define ALPHALAB_OPERATIONS_CHANGE_GUARD_MQH
bool ALOpsIsForbiddenHotField(const string field_name){ return field_name=="active_generation_bytes"||field_name=="live_feature_order"||field_name=="open_position_identity"||field_name=="reservation_ledger"; }
bool ALOpsIsQualificationInvalidatingField(const string field_name){ return field_name=="source_commit"||field_name=="release_manifest_hash"||field_name=="environment_hash"||field_name=="generation_hash"||field_name=="broker_server_hash"||field_name=="account_hashes"||field_name=="symbol_spec_hash"||field_name=="model_hash"||field_name=="policy_graph_hash"||field_name=="risk_envelope_hash"; }
#endif
