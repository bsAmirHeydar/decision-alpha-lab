#ifndef ALPHALAB_UCEI16_BOUNDARY_MQH
#define ALPHALAB_UCEI16_BOUNDARY_MQH
bool UCEI16_HasTradingAuthority(){ return false; }
bool UCEI16_HasNetworkAuthority(){ return false; }
bool UCEI16_RequiresKnownTime(){ return true; }
bool UCEI16_RequiresSharedEconomics(){ return true; }
#endif
