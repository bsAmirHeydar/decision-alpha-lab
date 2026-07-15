#ifndef __ALPHALAB_SAEDV4ACTIONLATTICESTATICVALIDATION_MQH__
#define __ALPHALAB_SAEDV4ACTIONLATTICESTATICVALIDATION_MQH__

// SAED V4-07 diagnostic-only mirror. No trading, file, socket or network authority.
bool SAEDV407ValidateEdge(const SAEDV407LatticeEdge &edge){ if(edge.source_node_id==edge.target_node_id) return false; if(edge.edge_kind==SAED_V4_07_ATOMIC_STEP && !SAEDV407IsAdjacent(edge.from_index,edge.to_index)) return false; return true; }

#endif // __ALPHALAB_SAEDV4ACTIONLATTICESTATICVALIDATION_MQH__
