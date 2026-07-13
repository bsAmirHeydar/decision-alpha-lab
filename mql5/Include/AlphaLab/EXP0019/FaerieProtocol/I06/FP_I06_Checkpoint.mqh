#ifndef __FP_I06_CHECKPOINT_MQH__
#define __FP_I06_CHECKPOINT_MQH__
struct FP_I06_Checkpoint { string checkpoint_id; string checkpoint_version; string config_hash; string source_revision_id; string compiler_report_hash; string snapshot_semantic_hash; string payload_hash; long created_utc_ms; bool Valid(string expected_config,string expected_revision,string expected_compiler) const {return checkpoint_version=="1.0.0" && config_hash==expected_config && source_revision_id==expected_revision && compiler_report_hash==expected_compiler && payload_hash!="";} };
#endif
