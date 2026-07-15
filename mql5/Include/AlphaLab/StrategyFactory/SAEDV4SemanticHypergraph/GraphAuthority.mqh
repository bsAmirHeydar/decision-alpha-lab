#ifndef ALPHA_LAB_SAED_V4_HYPERGRAPH_AUTHORITY_MQH
#define ALPHA_LAB_SAED_V4_HYPERGRAPH_AUTHORITY_MQH

struct SAEDHypergraphAuthorityBoundary
  {
   bool read_multimodal_package;
   bool read_view_lineage;
   bool build_hypergraph;
   bool replay_hypergraph;
   bool query_hypergraph;
   bool project_baseline;
   bool mutate_ucee_truth;
   bool mutate_view_artifacts;
   bool infer_canonical_relations;
   bool fit_adaptive_statistics;
   bool learn_edges;
   bool train_model;
   bool generate_treatment;
   bool select_treatment;
   bool allocate_risk;
   bool activate_runtime;
   bool send_order;
   bool network_access;
  };

void SAEDHypergraphDefaultAuthority(SAEDHypergraphAuthorityBoundary &authority)
  {
   authority.read_multimodal_package=true;
   authority.read_view_lineage=true;
   authority.build_hypergraph=true;
   authority.replay_hypergraph=true;
   authority.query_hypergraph=true;
   authority.project_baseline=true;
   authority.mutate_ucee_truth=false;
   authority.mutate_view_artifacts=false;
   authority.infer_canonical_relations=false;
   authority.fit_adaptive_statistics=false;
   authority.learn_edges=false;
   authority.train_model=false;
   authority.generate_treatment=false;
   authority.select_treatment=false;
   authority.allocate_risk=false;
   authority.activate_runtime=false;
   authority.send_order=false;
   authority.network_access=false;
  }

bool SAEDHypergraphAuthorityValid(const SAEDHypergraphAuthorityBoundary &authority)
  {
   if(!authority.read_multimodal_package || !authority.read_view_lineage || !authority.build_hypergraph)
      return false;
   if(!authority.replay_hypergraph || !authority.query_hypergraph || !authority.project_baseline)
      return false;
   if(authority.mutate_ucee_truth || authority.mutate_view_artifacts || authority.infer_canonical_relations)
      return false;
   if(authority.fit_adaptive_statistics || authority.learn_edges || authority.train_model)
      return false;
   if(authority.generate_treatment || authority.select_treatment || authority.allocate_risk)
      return false;
   if(authority.activate_runtime || authority.send_order || authority.network_access)
      return false;
   return true;
  }

#endif
