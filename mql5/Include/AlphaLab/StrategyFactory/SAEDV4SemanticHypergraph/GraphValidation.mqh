#ifndef ALPHA_LAB_SAED_V4_HYPERGRAPH_VALIDATION_MQH
#define ALPHA_LAB_SAED_V4_HYPERGRAPH_VALIDATION_MQH

#include "GraphContracts.mqh"
#include "GraphCanonical.mqh"
#include "GraphRegistry.mqh"
#include "GraphTemporal.mqh"

bool SAEDHypergraphNodeValid(const SAEDTemporalHypergraphNode &node,
                             const datetime event_as_of,
                             const datetime known_as_of)
  {
   if(StringLen(node.node_id)==0 || StringLen(node.semantic_key)==0)
      return false;
   if(node.quality<0.0 || node.quality>1.0)
      return false;
   if(!SAEDHypergraphBoundaryVisible(node.event_time,node.known_time,event_as_of,known_as_of))
      return false;
   if(!SAEDHypergraphIsHex64(node.node_hash))
      return false;
   return true;
  }

bool SAEDHypergraphEdgeValid(const SAEDTemporalHyperedge &edge,
                             const datetime event_as_of,
                             const datetime known_as_of)
  {
   if(StringLen(edge.edge_id)==0 || !SAEDHypergraphRelationKnown((int)edge.relation_kind))
      return false;
   if(!SAEDHypergraphRelationArityValid(edge.relation_kind,edge.arity))
      return false;
   if(!SAEDHypergraphIntervalValid(edge.event_time_start,edge.event_time_end,edge.known_time,event_as_of,known_as_of))
      return false;
   if(edge.mask!=0 && edge.mask!=1)
      return false;
   if(edge.active && edge.mask!=0)
      return false;
   if(!edge.active && edge.mask!=1)
      return false;
   if(edge.quality<0.0 || edge.quality>1.0)
      return false;
   if(!SAEDHypergraphIsHex64(edge.edge_hash))
      return false;
   return true;
  }

bool SAEDHypergraphHeaderValid(const SAEDSemanticTemporalHypergraphHeader &header)
  {
   if(StringLen(header.graph_id)==0 || StringLen(header.source_package_id)==0)
      return false;
   if(header.known_as_of<header.event_as_of)
      return false;
   if(header.node_count<1 || header.edge_count<1)
      return false;
   if(header.active_edge_count<0 || header.active_edge_count>header.edge_count)
      return false;
   if(!SAEDHypergraphIsHex64(header.graph_hash))
      return false;
   if(!SAEDHypergraphIsHex64(header.source_package_hash))
      return false;
   return true;
  }

#endif
