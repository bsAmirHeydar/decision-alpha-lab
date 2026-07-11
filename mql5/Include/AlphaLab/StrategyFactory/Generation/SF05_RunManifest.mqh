#ifndef __SF05_RUN_MANIFEST_MQH__
#define __SF05_RUN_MANIFEST_MQH__
#include "../Contracts/SF01_AllContracts.mqh"
#include "../Core/SF02_RuntimeConfig.mqh"
#include "../Plugins/SF04_PluginSelection.mqh"
#include "SF05_ResultSinkConfig.mqh"

struct SF05_RunManifest
{
   string schema;
   string manifest_id;
   string run_id;
   string strategy_id;
   string strategy_version;
   ENUM_SF02_RUN_MODE run_mode;
   long requested_generation_id;
   SF04_PluginSelection plugin_selection;
   string plugin_configuration_hash;
   string market_configuration_hash;
   SF05_ResultSinkConfig sink_config;
   string git_commit;
   string build_id;
   string environment_id;
   string terminal_instance_id;
   bool strict_fail_closed;
   SF01_MarketTimestamp created_at;
};

string SF05_RunManifestCanonical(const SF05_RunManifest &v)
{
   return v.schema+"|"+v.run_id+"|"+v.strategy_id+"|"+v.strategy_version+"|"+
          IntegerToString((int)v.run_mode)+"|"+LongToString(v.requested_generation_id)+"|"+
          v.plugin_selection.plugin_id+"|"+v.plugin_selection.exact_version+"|"+
          LongToString((long)v.plugin_selection.required_capabilities)+"|"+
          v.plugin_selection.expected_descriptor_hash+"|"+v.plugin_configuration_hash+"|"+
          v.market_configuration_hash+"|"+SF05_ResultSinkConfigHash(v.sink_config)+"|"+
          v.git_commit+"|"+v.build_id+"|"+v.environment_id+"|"+
          v.terminal_instance_id+"|"+SF01_CanonicalBool(v.strict_fail_closed)+"|"+
          LongToString(v.created_at.utc_epoch_milliseconds);
}

string SF05_DeriveRunManifestId(const SF05_RunManifest &v)
{
   return SF01_StableId("man",SF05_RunManifestCanonical(v));
}

bool SF05_ValidateRunManifest(const SF05_RunManifest &v,string &e)
{
   if(v.schema!="alpha_lab.strategy_factory/run_manifest@1.0.0"){e="unsupported run manifest schema";return false;}
   if(!SF01_IsSafeIdentifier(v.run_id,128)){e="invalid run_id";return false;}
   if(!SF01_IsSafeIdentifier(v.strategy_id,128)){e="invalid strategy_id";return false;}
   if(!SF01_IsSafeIdentifier(v.strategy_version,64)){e="invalid strategy_version";return false;}
   if(v.requested_generation_id<=0){e="generation id must be positive";return false;}
   if(!SF04_ValidatePluginSelection(v.plugin_selection,e))return false;
   if(!SF01_IsSafeIdentifier(v.plugin_configuration_hash,128)){e="invalid plugin configuration hash";return false;}
   if(!SF01_IsSafeIdentifier(v.market_configuration_hash,128)){e="invalid market configuration hash";return false;}
   if(!SF05_ValidateResultSinkConfig(v.sink_config,e))return false;
   if(!SF01_IsSafeIdentifier(v.git_commit,128)){e="invalid git_commit";return false;}
   if(!SF01_IsSafeIdentifier(v.build_id,128)){e="invalid build_id";return false;}
   if(!SF01_IsSafeIdentifier(v.environment_id,128)){e="invalid environment_id";return false;}
   if(!SF01_IsSafeIdentifier(v.terminal_instance_id,128)){e="invalid terminal instance id";return false;}
   if(!SF01_ValidateTimestamp(v.created_at,e))return false;
   string expected=SF05_DeriveRunManifestId(v);
   if(v.manifest_id!=""&&v.manifest_id!=expected){e="manifest_id mismatch";return false;}
   e="";return true;
}

string SF05_RunManifestToJson(const SF05_RunManifest &v)
{
   string id=v.manifest_id==""?SF05_DeriveRunManifestId(v):v.manifest_id;
   return "{\"schema\":\""+SF01_JsonEscape(v.schema)+"\",\"manifest_id\":\""+id+
          "\",\"run_id\":\""+SF01_JsonEscape(v.run_id)+"\",\"strategy_id\":\""+
          SF01_JsonEscape(v.strategy_id)+"\",\"strategy_version\":\""+
          SF01_JsonEscape(v.strategy_version)+"\",\"run_mode\":\""+
          SF02_RunModeToString(v.run_mode)+"\",\"requested_generation_id\":"+
          LongToString(v.requested_generation_id)+",\"plugin_id\":\""+
          SF01_JsonEscape(v.plugin_selection.plugin_id)+"\",\"plugin_version\":\""+
          SF01_JsonEscape(v.plugin_selection.exact_version)+"\",\"plugin_configuration_hash\":\""+
          SF01_JsonEscape(v.plugin_configuration_hash)+"\",\"market_configuration_hash\":\""+
          SF01_JsonEscape(v.market_configuration_hash)+"\",\"sink_configuration_hash\":\""+
          SF05_ResultSinkConfigHash(v.sink_config)+"\",\"git_commit\":\""+
          SF01_JsonEscape(v.git_commit)+"\",\"build_id\":\""+SF01_JsonEscape(v.build_id)+
          "\",\"environment_id\":\""+SF01_JsonEscape(v.environment_id)+
          "\",\"terminal_instance_id\":\""+SF01_JsonEscape(v.terminal_instance_id)+
          "\",\"strict_fail_closed\":"+SF01_CanonicalBool(v.strict_fail_closed)+
          ",\"created_at\":"+SF01_TimestampToJson(v.created_at)+"}";
}
#endif
