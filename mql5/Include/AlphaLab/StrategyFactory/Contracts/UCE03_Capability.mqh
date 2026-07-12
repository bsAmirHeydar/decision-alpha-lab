#ifndef __UCE03_CAPABILITY_MQH__
#define __UCE03_CAPABILITY_MQH__
#include "UCE03_Enums.mqh"
struct UCE03_ResourceBudget
{
   int max_features;
   int max_sequence_length;
   int max_batch_size;
   int max_memory_mb;
   long max_latency_us;
};
struct UCE03_CapabilityDescriptor
{
   string component_id;
   string component_version;
   string support_level;
   string context_kinds_csv;
   string representation_kinds_csv;
   string task_types_csv;
   string treatment_families_csv;
   string runtime_modes_csv;
   string export_targets_csv;
   string input_schema_ids_csv;
   string output_schema_ids_csv;
   bool supports_missing_values;
   bool supports_sample_weights;
   bool supports_multitask;
   bool deterministic;
   UCE03_ResourceBudget resource_budget;
};
int UCE03_SupportLevelRank(const string value)
{
   if(value=="experimental")return 0;
   if(value=="research")return 1;
   if(value=="paper")return 2;
   if(value=="production")return 3;
   return -1;
}
bool UCE03_CsvContainsToken(const string csv,const string token)
{
   const string wrapped=","+csv+",";return StringFind(wrapped,","+token+",")>=0;
}
#endif
