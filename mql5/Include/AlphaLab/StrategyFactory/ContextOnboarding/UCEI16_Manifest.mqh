#ifndef ALPHALAB_UCEI16_MANIFEST_MQH
#define ALPHALAB_UCEI16_MANIFEST_MQH
struct UCEI16_Artifact { string path; string content_hash; string kind; };
struct UCEI16_Manifest { string manifest_id; string context_id; string context_spec_hash; string tournament_template_hash; string core_snapshot_hash; int artifact_count; };
bool UCEI16_ValidateManifest(const UCEI16_Manifest &m){ return StringLen(m.manifest_id)>0 && StringLen(m.context_id)>0 && StringLen(m.context_spec_hash)==64 && StringLen(m.tournament_template_hash)==64 && StringLen(m.core_snapshot_hash)==64 && m.artifact_count>=15; }
#endif
