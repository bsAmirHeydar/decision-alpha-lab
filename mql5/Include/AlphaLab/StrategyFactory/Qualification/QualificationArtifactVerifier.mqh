#ifndef ALPHALAB_QUALIFICATION_ARTIFACT_VERIFIER_MQH
#define ALPHALAB_QUALIFICATION_ARTIFACT_VERIFIER_MQH
bool ALArtifactIdentityLooksValid(const string artifact_id,const string artifact_hash,const string schema_version){ return StringLen(artifact_id)>0 && StringLen(artifact_hash)==64 && schema_version=="1.0.0"; }
#endif
