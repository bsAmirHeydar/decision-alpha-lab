#ifndef ALPHALAB_PORTFOLIO_INTERACTION_MQH
#define ALPHALAB_PORTFOLIO_INTERACTION_MQH
bool ALDirectionConflict(const string symbol_a,const int side_a,const string symbol_b,const int side_b){ return symbol_a==symbol_b && side_a!=side_b; }
#endif
