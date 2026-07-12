#ifndef __UCE03_COMPATIBILITY_MQH__
#define __UCE03_COMPATIBILITY_MQH__
#include "UCE03_Capability.mqh"
#include "UCE03_Migration.mqh"
struct UCE03_CompatibilityRequest
{
   string component_id;
   string context_kind;
   string representation_kind;
   string task_type;
   string treatment_family;
   string runtime_mode;
   string export_target;
   string minimum_support_level;
   UCE03_SchemaId input_schema;
   UCE03_SchemaId required_output_schema;
   int feature_count;
   int sequence_length;
   int batch_size;
   int estimated_memory_mb;
   long latency_budget_us;
   bool requires_missing_values;
   bool requires_sample_weights;
   bool requires_multitask;
   bool requires_determinism;
};
struct UCE03_CompatibilityDecision
{
   ENUM_UCE03_COMPATIBILITY_STATUS status;
   string reason_codes_csv;
   string migration_path_csv;
};
void UCE03_AddReason(string &csv,const string code){if(csv!="")csv+=",";csv+=code;}
UCE03_CompatibilityDecision UCE03_EvaluateCompatibility(const UCE03_CapabilityDescriptor &capability,const UCE03_CompatibilityRequest &request,CUCE03SchemaRegistry &schemas,CUCE03MigrationRegistry &migrations)
{
   UCE03_CompatibilityDecision result;result.status=UCE03_INCOMPATIBLE;result.reason_codes_csv="";result.migration_path_csv="";
   if(request.component_id!=capability.component_id)UCE03_AddReason(result.reason_codes_csv,"component_id_mismatch");
   if(UCE03_SupportLevelRank(capability.support_level)<UCE03_SupportLevelRank(request.minimum_support_level))UCE03_AddReason(result.reason_codes_csv,"support_level_insufficient");
   if(!UCE03_CsvContainsToken(capability.context_kinds_csv,request.context_kind))UCE03_AddReason(result.reason_codes_csv,"context_kind_unsupported");
   if(!UCE03_CsvContainsToken(capability.representation_kinds_csv,request.representation_kind))UCE03_AddReason(result.reason_codes_csv,"representation_unsupported");
   if(!UCE03_CsvContainsToken(capability.task_types_csv,request.task_type))UCE03_AddReason(result.reason_codes_csv,"task_unsupported");
   if(!UCE03_CsvContainsToken(capability.treatment_families_csv,request.treatment_family))UCE03_AddReason(result.reason_codes_csv,"treatment_unsupported");
   if(!UCE03_CsvContainsToken(capability.runtime_modes_csv,request.runtime_mode))UCE03_AddReason(result.reason_codes_csv,"runtime_mode_unsupported");
   if(!UCE03_CsvContainsToken(capability.export_targets_csv,request.export_target))UCE03_AddReason(result.reason_codes_csv,"export_target_unsupported");
   if(request.feature_count>capability.resource_budget.max_features)UCE03_AddReason(result.reason_codes_csv,"feature_budget_exceeded");
   if(request.sequence_length>capability.resource_budget.max_sequence_length)UCE03_AddReason(result.reason_codes_csv,"sequence_budget_exceeded");
   if(request.batch_size>capability.resource_budget.max_batch_size)UCE03_AddReason(result.reason_codes_csv,"batch_budget_exceeded");
   if(request.estimated_memory_mb>capability.resource_budget.max_memory_mb)UCE03_AddReason(result.reason_codes_csv,"memory_budget_exceeded");
   if(request.latency_budget_us>capability.resource_budget.max_latency_us)UCE03_AddReason(result.reason_codes_csv,"latency_budget_exceeded");
   if(request.requires_missing_values&&!capability.supports_missing_values)UCE03_AddReason(result.reason_codes_csv,"missing_values_unsupported");
   if(request.requires_sample_weights&&!capability.supports_sample_weights)UCE03_AddReason(result.reason_codes_csv,"sample_weights_unsupported");
   if(request.requires_multitask&&!capability.supports_multitask)UCE03_AddReason(result.reason_codes_csv,"multitask_unsupported");
   if(request.requires_determinism&&!capability.deterministic)UCE03_AddReason(result.reason_codes_csv,"determinism_required");
   UCE03_SchemaDescriptor output_descriptor;
   if(!UCE03_CsvContainsToken(capability.output_schema_ids_csv,UCE03_SchemaExactKey(request.required_output_schema)))UCE03_AddReason(result.reason_codes_csv,"output_schema_unsupported");
   if(!schemas.ResolveExact(request.required_output_schema,output_descriptor))UCE03_AddReason(result.reason_codes_csv,"required_output_schema_unknown");
   const string input_exact=UCE03_SchemaExactKey(request.input_schema);
   UCE03_SchemaDescriptor input_descriptor;
   if(!schemas.ResolveExact(request.input_schema,input_descriptor))UCE03_AddReason(result.reason_codes_csv,"input_schema_unknown");
   if(!UCE03_CsvContainsToken(capability.input_schema_ids_csv,input_exact))
   {
      UCE03_MigrationEdge migration_edge;
      if(migrations.FindDirectToCsv(request.input_schema,capability.input_schema_ids_csv,migration_edge))
         result.migration_path_csv=migration_edge.migration_id;
      else
         UCE03_AddReason(result.reason_codes_csv,"input_schema_unsupported_and_unmigratable");
   }
   if(result.reason_codes_csv!="")return result;
   result.status=(result.migration_path_csv=="")?UCE03_COMPATIBLE:UCE03_COMPATIBLE_AFTER_MIGRATION;
   return result;
}
#endif
