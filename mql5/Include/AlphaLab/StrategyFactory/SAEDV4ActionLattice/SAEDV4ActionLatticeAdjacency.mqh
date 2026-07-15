#ifndef __ALPHALAB_SAEDV4ACTIONLATTICEADJACENCY_MQH__
#define __ALPHALAB_SAEDV4ACTIONLATTICEADJACENCY_MQH__

// SAED V4-07 diagnostic-only mirror. No trading, file, socket or network authority.
bool SAEDV407IsAdjacent(const int from_index,const int to_index){ return to_index-from_index==1; }

#endif // __ALPHALAB_SAEDV4ACTIONLATTICEADJACENCY_MQH__
