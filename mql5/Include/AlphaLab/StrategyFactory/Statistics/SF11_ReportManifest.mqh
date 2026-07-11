#ifndef __SF11_REPORT_MANIFEST_MQH__
#define __SF11_REPORT_MANIFEST_MQH__
#include "SF11_MatchedNullEngine.mqh"
struct SF11_StatisticalReportManifest
{
   string schema;string report_id;string report_program_id;string report_version;string source_run_id;string source_manifest_hash;string source_artifact_hash;string strategy_id;string strategy_version;string candidate_matrix_hash;string simulation_policy_hash;string cost_registry_hash;string group_schema_hash;string metric_registry_hash;string null_registry_hash;int random_seed;long generated_at_utc_msc;string git_commit;string manifest_hash;
};
string SF11_ReportManifestCanonical(const SF11_StatisticalReportManifest &m)
{
   return m.schema+"|"+m.report_id+"|"+m.report_program_id+"|"+m.report_version+"|"+m.source_run_id+"|"+m.source_manifest_hash+"|"+m.source_artifact_hash+"|"+m.strategy_id+"|"+m.strategy_version+"|"+m.candidate_matrix_hash+"|"+m.simulation_policy_hash+"|"+m.cost_registry_hash+"|"+m.group_schema_hash+"|"+m.metric_registry_hash+"|"+m.null_registry_hash+"|"+IntegerToString(m.random_seed)+"|"+IntegerToString(m.generated_at_utc_msc)+"|"+m.git_commit;
}
string SF11_DeriveReportManifestHash(const SF11_StatisticalReportManifest &m){return SF01_StableId("srep",SF11_ReportManifestCanonical(m));}
bool SF11_ValidateReportManifest(const SF11_StatisticalReportManifest &m,string &error)
{
   if(m.schema!="alpha_lab.strategy_factory/statistical_report_manifest@1.0.0"){error="unsupported statistical report manifest schema";return false;}
   if(!SF01_IsSafeIdentifier(m.report_id,128)||!SF01_IsSafeIdentifier(m.report_program_id,128)||!SF01_IsSafeIdentifier(m.report_version,64)||!SF01_IsSafeIdentifier(m.source_run_id,128)||!SF01_IsSafeIdentifier(m.source_manifest_hash,128)||!SF01_IsSafeIdentifier(m.source_artifact_hash,128)||!SF01_IsSafeIdentifier(m.strategy_id,128)||!SF01_IsSafeIdentifier(m.strategy_version,64)||!SF01_IsSafeIdentifier(m.git_commit,128)||m.generated_at_utc_msc<0){error="invalid statistical report manifest";return false;}
   const string expected=SF11_DeriveReportManifestHash(m);if(m.manifest_hash!=""&&m.manifest_hash!=expected){error="statistical report manifest hash mismatch";return false;}error="";return true;
}
#endif
