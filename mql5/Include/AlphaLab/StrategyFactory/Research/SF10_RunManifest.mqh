#ifndef __SF10_RUN_MANIFEST_MQH__
#define __SF10_RUN_MANIFEST_MQH__
#include "SF10_ResearchEnums.mqh"
#include "../Generation/SF05_RunManifest.mqh"

struct SF10_RunManifest
{
   string schema;
   string run_id;
   string research_program_id;
   string strategy_id;
   string strategy_version;
   long runtime_generation_id;
   string runtime_generation_hash;
   string plugin_set_hash;
   string candidate_matrix_hash;
   string simulation_policy_hash;
   string cost_registry_hash;
   string input_parameter_hash;
   string data_source_id;
   string symbol;
   int timeframe_seconds;
   long test_start_utc_msc;
   long test_end_utc_msc;
   ENUM_SF10_FIDELITY_PRESET fidelity_preset;
   ENUM_SF10_OBJECTIVE_MODE objective_mode;
   ENUM_SF10_EXPORT_DETAIL export_detail;
   int random_seed;
   string git_commit;
   string terminal_build;
   string source_hash;
   string manifest_hash;
};

string SF10_RunManifestCanonical(const SF10_RunManifest &m)
{
   return m.schema+"|"+m.run_id+"|"+m.research_program_id+"|"+m.strategy_id+"|"+
          m.strategy_version+"|"+IntegerToString(m.runtime_generation_id)+"|"+
          m.runtime_generation_hash+"|"+m.plugin_set_hash+"|"+m.candidate_matrix_hash+"|"+
          m.simulation_policy_hash+"|"+m.cost_registry_hash+"|"+m.input_parameter_hash+"|"+
          m.data_source_id+"|"+m.symbol+"|"+IntegerToString(m.timeframe_seconds)+"|"+
          IntegerToString(m.test_start_utc_msc)+"|"+IntegerToString(m.test_end_utc_msc)+"|"+
          IntegerToString((int)m.fidelity_preset)+"|"+IntegerToString((int)m.objective_mode)+"|"+
          IntegerToString((int)m.export_detail)+"|"+IntegerToString(m.random_seed)+"|"+
          m.git_commit+"|"+m.terminal_build+"|"+m.source_hash;
}

string SF10_DeriveRunManifestHash(const SF10_RunManifest &m)
{return SF01_StableId("rman",SF10_RunManifestCanonical(m));}

bool SF10_ValidateRunManifest(const SF10_RunManifest &m,string &error)
{
   if(m.schema!="alpha_lab.strategy_factory/research_run_manifest@1.0.0")
   {error="unsupported research run manifest schema";return false;}
   if(!SF01_IsSafeIdentifier(m.run_id,128)||!SF01_IsSafeIdentifier(m.research_program_id,128)||
      !SF01_IsSafeIdentifier(m.strategy_id,128)||!SF01_IsSafeIdentifier(m.strategy_version,64)||
      !SF01_IsSafeIdentifier(m.runtime_generation_hash,128)||!SF01_IsSafeIdentifier(m.plugin_set_hash,128)||
      !SF01_IsSafeIdentifier(m.candidate_matrix_hash,128)||!SF01_IsSafeIdentifier(m.simulation_policy_hash,128)||
      !SF01_IsSafeIdentifier(m.cost_registry_hash,128)||!SF01_IsSafeIdentifier(m.input_parameter_hash,128)||
      !SF01_IsSafeIdentifier(m.data_source_id,128)||!SF01_IsTerminalSymbol(m.symbol)||
      !SF01_IsSafeIdentifier(m.git_commit,128)||!SF01_IsSafeIdentifier(m.source_hash,128))
   {error="invalid run manifest identity";return false;}
   if(m.runtime_generation_id<0||m.timeframe_seconds<=0||m.test_start_utc_msc<0||
      m.test_end_utc_msc<=m.test_start_utc_msc)
   {error="invalid run manifest range";return false;}
   const string expected=SF10_DeriveRunManifestHash(m);
   if(m.manifest_hash!=""&&m.manifest_hash!=expected)
   {error="run manifest hash mismatch";return false;}
   error="";return true;
}
#endif
