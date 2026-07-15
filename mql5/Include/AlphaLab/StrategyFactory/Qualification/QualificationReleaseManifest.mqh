#ifndef ALPHALAB_QUALIFICATION_RELEASE_MANIFEST_MQH
#define ALPHALAB_QUALIFICATION_RELEASE_MANIFEST_MQH
#include "QualificationEnums.mqh"
struct ALReleaseManifest { string manifest_id; string qualification_hash; string generation_hash; string rollback_generation_hash; ALReleaseStage stage; bool order_authority; bool broker_authority; double max_risk; string approved_by; long approved_at_ms; long expires_at_ms; };
bool ALReleaseManifestIsSafe(const ALReleaseManifest &manifest,const long now_ms){ if(StringLen(manifest.qualification_hash)!=64 || StringLen(manifest.generation_hash)!=64 || StringLen(manifest.rollback_generation_hash)!=64) return false; if(StringLen(manifest.approved_by)==0 || manifest.expires_at_ms<=now_ms || manifest.approved_at_ms>now_ms) return false; if((manifest.stage==AL_STAGE_PAPER || manifest.stage==AL_STAGE_SHADOW) && (manifest.order_authority || manifest.broker_authority || manifest.max_risk!=0.0)) return false; if((manifest.order_authority || manifest.broker_authority) && manifest.stage<AL_STAGE_MICRO_LIVE) return false; return true; }
#endif
