#ifndef ALPHALAB_UCEI07_ARTIFACT_VALIDATOR_MQH
#define ALPHALAB_UCEI07_ARTIFACT_VALIDATOR_MQH
#include "UCEI07_Contracts.mqh"
class CUCEI07ArtifactValidator{
public:
 bool ValidateState(const UCEI07_ModelStateBundle &state,string &reason)const{reason="";if(state.trainer_key==""||state.state_format==""||state.state_payload==""||state.state_hash==""){reason="incomplete_model_state";return false;}if(state.state_format!="canonical_json"&&state.state_format!="onnx"&&state.state_format!="native_text"){reason="opaque_or_unsupported_state_format";return false;}return true;}
 bool ValidateManifest(const UCEI07_ArtifactManifest &m,string &reason)const{reason="";if(m.artifact_id==""||m.artifact_version==""||m.trainer_descriptor_hash==""||m.trainer_config_hash==""||m.task_contract_hash==""||m.dataset_manifest_hash==""||m.state_hash==""){reason="incomplete_artifact_lineage";return false;}if(m.feature_order==""||m.output_names==""){reason="missing_io_contract";return false;}return true;}
};
#endif
