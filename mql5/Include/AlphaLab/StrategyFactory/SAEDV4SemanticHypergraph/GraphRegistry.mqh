#ifndef ALPHA_LAB_SAED_V4_HYPERGRAPH_REGISTRY_MQH
#define ALPHA_LAB_SAED_V4_HYPERGRAPH_REGISTRY_MQH

#include "GraphEnums.mqh"

int SAEDHypergraphInstitutionalNodeKindCount()
  {
   return 7;
  }

int SAEDHypergraphInstitutionalRelationKindCount()
  {
   return 8;
  }

bool SAEDHypergraphRelationArityValid(const ENUM_SAED_HYPERGRAPH_RELATION_KIND kind,const int arity)
  {
   if(arity<2)
      return false;
   if(kind==SAED_HREL_CROSS_VIEW_ALIGNMENT && arity<3)
      return false;
   if(arity>512)
      return false;
   return true;
  }

bool SAEDHypergraphRelationKnown(const int kind)
  {
   return (kind>=SAED_HREL_CONTEXT_COMPOSITION && kind<=SAED_HREL_TREATMENT_DESCRIPTOR_BINDING);
  }

#endif
