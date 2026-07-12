#ifndef __UCE03_ENUMS_MQH__
#define __UCE03_ENUMS_MQH__
enum ENUM_UCE03_IDENTITY_KIND
{
   UCE03_ID_CONTEXT_OCCURRENCE=0,
   UCE03_ID_CONTEXT_CLUSTER=1,
   UCE03_ID_PARENT_EVENT=2,
   UCE03_ID_REPRESENTATION_VIEW=3,
   UCE03_ID_TREATMENT_ATOM=4,
   UCE03_ID_COMPLETE_TREATMENT=5,
   UCE03_ID_TASK=6,
   UCE03_ID_DATASET_ROW=7,
   UCE03_ID_EXPERIMENT_TRIAL=8,
   UCE03_ID_PREDICTION=9,
   UCE03_ID_MODEL=10,
   UCE03_ID_POLICY=11,
   UCE03_ID_RUNTIME_GENERATION=12,
   UCE03_ID_EVIDENCE_BUNDLE=13
};
enum ENUM_UCE03_COMPATIBILITY_STATUS
{
   UCE03_COMPATIBLE=0,
   UCE03_COMPATIBLE_AFTER_MIGRATION=1,
   UCE03_INCOMPATIBLE=2
};
enum ENUM_UCE03_RUNTIME_MODE { UCE03_RESEARCH=0, UCE03_TESTER=1, UCE03_PAPER=2, UCE03_SHADOW=3, UCE03_LIVE=4 };
string UCE03_IdentityKindName(const ENUM_UCE03_IDENTITY_KIND value)
{
   switch(value)
   {
      case UCE03_ID_CONTEXT_OCCURRENCE:return "context_occurrence";
      case UCE03_ID_CONTEXT_CLUSTER:return "context_cluster";
      case UCE03_ID_PARENT_EVENT:return "parent_event";
      case UCE03_ID_REPRESENTATION_VIEW:return "representation_view";
      case UCE03_ID_TREATMENT_ATOM:return "treatment_atom";
      case UCE03_ID_COMPLETE_TREATMENT:return "complete_treatment";
      case UCE03_ID_TASK:return "task";
      case UCE03_ID_DATASET_ROW:return "dataset_row";
      case UCE03_ID_EXPERIMENT_TRIAL:return "experiment_trial";
      case UCE03_ID_PREDICTION:return "prediction";
      case UCE03_ID_MODEL:return "model";
      case UCE03_ID_POLICY:return "policy";
      case UCE03_ID_RUNTIME_GENERATION:return "runtime_generation";
      case UCE03_ID_EVIDENCE_BUNDLE:return "evidence_bundle";
   }
   return "unknown";
}
#endif
