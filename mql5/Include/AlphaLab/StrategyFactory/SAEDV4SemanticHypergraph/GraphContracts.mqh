#ifndef ALPHA_LAB_SAED_V4_HYPERGRAPH_CONTRACTS_MQH
#define ALPHA_LAB_SAED_V4_HYPERGRAPH_CONTRACTS_MQH

#include "GraphEnums.mqh"
#include "GraphAuthority.mqh"

struct SAEDTemporalHypergraphNode
  {
   string node_id;
   ENUM_SAED_HYPERGRAPH_NODE_KIND kind;
   string semantic_key;
   datetime event_time;
   datetime known_time;
   double quality;
   bool missing;
   bool masked;
   string source_hash;
   string node_hash;
  };

struct SAEDTemporalHyperedge
  {
   string edge_id;
   ENUM_SAED_HYPERGRAPH_RELATION_KIND relation_kind;
   string member_node_ids;
   int arity;
   datetime event_time_start;
   datetime event_time_end;
   datetime known_time;
   bool active;
   int mask;
   double quality;
   string source_rule_id;
   string edge_hash;
  };

struct SAEDSemanticTemporalHypergraphHeader
  {
   string graph_id;
   string graph_version;
   string registry_id;
   string registry_hash;
   string policy_id;
   string policy_hash;
   string source_package_id;
   string source_package_hash;
   string twin_id;
   datetime known_as_of;
   datetime event_as_of;
   ENUM_SAED_HYPERGRAPH_STATUS status;
   int node_count;
   int edge_count;
   int active_edge_count;
   string lineage_root;
   string graph_hash;
  };

#endif
