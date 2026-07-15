#property strict
#include <AlphaLab/StrategyFactory/SAEDV4ActionLattice/SAEDV4ActionLattice.mqh>
int OnInit(){ SAEDV407LatticeEdge e; e.source_node_id="a"; e.target_node_id="b"; e.edge_kind=SAED_V4_07_ATOMIC_STEP; e.from_index=0; e.to_index=1; Print("edge valid=",SAEDV407ValidateEdge(e)); return(INIT_SUCCEEDED); }
void OnTick(){}
