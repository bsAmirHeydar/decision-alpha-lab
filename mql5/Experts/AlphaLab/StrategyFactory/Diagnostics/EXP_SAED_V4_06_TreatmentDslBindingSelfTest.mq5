#property strict
#include <AlphaLab/StrategyFactory/SAEDV4TreatmentDsl/SAEDV4TreatmentDsl.mqh>

void OnStart()
  {
   SAEDV4DslBindingHeader value;
   value.binding_id="dslbinding_reference";
   value.binding_hash="0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef";
   value.descriptor_id="treatment_approved_001";
   value.graph_node_id="hnode_reference";
   value.graph_node_hash=value.binding_hash;
   value.program_id="treatment_reference";
   value.program_hash=value.binding_hash;
   value.bound=true;
   if(!SAEDV4DslBindingHeaderValid(value)) Print("SAED V4-06 binding self-test failed");
  }
