#ifndef __SF05_RUNTIME_GENERATION_MQH__
#define __SF05_RUNTIME_GENERATION_MQH__
#include "SF05_RunManifest.mqh"
#include "../Plugins/SF04_PluginDescriptor.mqh"
#include "../Plugins/SF04_PluginStartupValidator.mqh"

struct SF05_RuntimeGenerationRecord
{
   string schema;
   string generation_uid;
   long generation_id;
   ENUM_SF05_GENERATION_STATE state;
   string run_manifest_id;
   string run_manifest_hash;
   string plugin_descriptor_hash;
   string plugin_requirements_hash;
   string plugin_configuration_hash;
   string market_configuration_hash;
   string sink_configuration_hash;
   string compiler_id;
   string compiler_version;
   string previous_generation_uid;
   SF01_MarketTimestamp compiled_at;
   SF01_MarketTimestamp activated_at;
   SF01_MarketTimestamp retired_at;
   string failure_reason;
};

string SF05_RuntimeGenerationCanonical(const SF05_RuntimeGenerationRecord &v)
{
   return v.schema+"|"+IntegerToString(v.generation_id)+"|"+v.run_manifest_id+"|"+
          v.run_manifest_hash+"|"+v.plugin_descriptor_hash+"|"+v.plugin_requirements_hash+"|"+
          v.plugin_configuration_hash+"|"+v.market_configuration_hash+"|"+
          v.sink_configuration_hash+"|"+v.compiler_id+"|"+v.compiler_version+"|"+
          v.previous_generation_uid+"|"+IntegerToString(v.compiled_at.utc_epoch_milliseconds);
}

string SF05_DeriveGenerationUid(const SF05_RuntimeGenerationRecord &v)
{
   return SF01_StableId("gen",SF05_RuntimeGenerationCanonical(v));
}

bool SF05_ValidateRuntimeGeneration(const SF05_RuntimeGenerationRecord &v,string &e)
{
   if(v.schema!="alpha_lab.strategy_factory/runtime_generation@1.0.0"){e="unsupported generation schema";return false;}
   if(v.generation_id<=0){e="generation id must be positive";return false;}
   if(!SF01_IsSafeIdentifier(v.run_manifest_id,128)||!SF01_IsSafeIdentifier(v.run_manifest_hash,128)){e="invalid manifest identity";return false;}
   if(!SF01_IsSafeIdentifier(v.plugin_descriptor_hash,128)||!SF01_IsSafeIdentifier(v.plugin_requirements_hash,128)){e="invalid plugin evidence";return false;}
   if(!SF01_IsSafeIdentifier(v.plugin_configuration_hash,128)||!SF01_IsSafeIdentifier(v.market_configuration_hash,128)||!SF01_IsSafeIdentifier(v.sink_configuration_hash,128)){e="invalid configuration hash";return false;}
   if(!SF01_IsSafeIdentifier(v.compiler_id,128)||!SF01_IsSafeIdentifier(v.compiler_version,64)){e="invalid compiler identity";return false;}
   if(v.previous_generation_uid!=""&&!SF01_IsSafeIdentifier(v.previous_generation_uid,128)){e="invalid previous generation";return false;}
   if(!SF01_ValidateTimestamp(v.compiled_at,e))return false;
   string expected=SF05_DeriveGenerationUid(v);
   if(v.generation_uid!=""&&v.generation_uid!=expected){e="generation uid mismatch";return false;}
   e="";return true;
}

bool SF05_CanTransitionGeneration(const ENUM_SF05_GENERATION_STATE from,const ENUM_SF05_GENERATION_STATE to)
{
   if(from==SF05_GENERATION_DRAFT&&to==SF05_GENERATION_COMPILED)return true;
   if(from==SF05_GENERATION_COMPILED&&to==SF05_GENERATION_VALIDATED)return true;
   if(from==SF05_GENERATION_VALIDATED&&to==SF05_GENERATION_WARMED)return true;
   if(from==SF05_GENERATION_WARMED&&to==SF05_GENERATION_ACTIVE)return true;
   if(from==SF05_GENERATION_ACTIVE&&to==SF05_GENERATION_RETIRED)return true;
   if(from!=SF05_GENERATION_RETIRED&&to==SF05_GENERATION_FAILED)return true;
   return false;
}

bool SF05_TransitionGeneration(SF05_RuntimeGenerationRecord &v,const ENUM_SF05_GENERATION_STATE to,const SF01_MarketTimestamp &now,const string reason,string &e)
{
   if(!SF05_CanTransitionGeneration(v.state,to)){e="illegal generation transition "+SF05_GenerationStateToString(v.state)+"->"+SF05_GenerationStateToString(to);return false;}
   v.state=to;
   if(to==SF05_GENERATION_ACTIVE)v.activated_at=now;
   if(to==SF05_GENERATION_RETIRED)v.retired_at=now;
   if(to==SF05_GENERATION_FAILED)v.failure_reason=reason;
   e="";return true;
}

string SF05_RuntimeGenerationToJson(const SF05_RuntimeGenerationRecord &v)
{
   string id=v.generation_uid==""?SF05_DeriveGenerationUid(v):v.generation_uid;
   return "{\"schema\":\""+SF01_JsonEscape(v.schema)+"\",\"generation_uid\":\""+id+
          "\",\"generation_id\":"+IntegerToString(v.generation_id)+",\"state\":\""+
          SF05_GenerationStateToString(v.state)+"\",\"run_manifest_id\":\""+
          SF01_JsonEscape(v.run_manifest_id)+"\",\"run_manifest_hash\":\""+
          SF01_JsonEscape(v.run_manifest_hash)+"\",\"plugin_descriptor_hash\":\""+
          SF01_JsonEscape(v.plugin_descriptor_hash)+"\",\"plugin_requirements_hash\":\""+
          SF01_JsonEscape(v.plugin_requirements_hash)+"\",\"plugin_configuration_hash\":\""+
          SF01_JsonEscape(v.plugin_configuration_hash)+"\",\"market_configuration_hash\":\""+
          SF01_JsonEscape(v.market_configuration_hash)+"\",\"sink_configuration_hash\":\""+
          SF01_JsonEscape(v.sink_configuration_hash)+"\",\"compiler_id\":\""+
          SF01_JsonEscape(v.compiler_id)+"\",\"compiler_version\":\""+
          SF01_JsonEscape(v.compiler_version)+"\",\"previous_generation_uid\":\""+
          SF01_JsonEscape(v.previous_generation_uid)+"\",\"compiled_at\":"+
          SF01_TimestampToJson(v.compiled_at)+",\"activated_at\":"+
          SF01_TimestampToJson(v.activated_at)+",\"retired_at\":"+
          SF01_TimestampToJson(v.retired_at)+",\"failure_reason\":\""+
          SF01_JsonEscape(v.failure_reason)+"\"}";
}
#endif
