#ifndef ALPHA_LAB_SAED_V4_HYPERGRAPH_DIAGNOSTICS_MQH
#define ALPHA_LAB_SAED_V4_HYPERGRAPH_DIAGNOSTICS_MQH

#include "GraphAuthority.mqh"
#include "GraphRegistry.mqh"
#include "GraphProjection.mqh"

bool SAEDHypergraphStaticSelfTest()
  {
   SAEDHypergraphAuthorityBoundary authority;
   SAEDHypergraphDefaultAuthority(authority);
   if(!SAEDHypergraphAuthorityValid(authority))
      return false;
   if(SAEDHypergraphInstitutionalNodeKindCount()!=7)
      return false;
   if(SAEDHypergraphInstitutionalRelationKindCount()!=8)
      return false;
   if(!SAEDHypergraphRelationArityValid(SAED_HREL_CONTEXT_COMPOSITION,2))
      return false;
   if(SAEDHypergraphRelationArityValid(SAED_HREL_CROSS_VIEW_ALIGNMENT,2))
      return false;
   if(SAEDHypergraphIncidenceValue(true,true)!=1)
      return false;
   if(SAEDHypergraphIncidenceValue(false,true)!=-1)
      return false;
   return true;
  }

#endif
