#ifndef ALPHA_LAB_SAED_V4_HYPERGRAPH_PROJECTION_MQH
#define ALPHA_LAB_SAED_V4_HYPERGRAPH_PROJECTION_MQH

int SAEDHypergraphIncidenceValue(const bool edge_active,const bool member)
  {
   if(!member)
      return 0;
   return edge_active ? 1 : -1;
  }

bool SAEDHypergraphProjectionBudgetValid(const int node_count,
                                         const int edge_count,
                                         const long maximum_cells)
  {
   if(node_count<1 || edge_count<1 || maximum_cells<1)
      return false;
   long cells=(long)node_count*(long)edge_count;
   return cells<=maximum_cells;
  }

#endif
