#ifndef __FP_I09_RANKING_MQH__
#define __FP_I09_RANKING_MQH__
#include "FP_I09_Contracts.mqh"
int FP_I09_RelationRank(const string relation){ string a[7]={"AL","AN","LN","NA","NL","NN","WW"}; for(int i=0;i<7;i++) if(a[i]==relation) return i; return 99; }
int FP_I09_Compare(const FP_I09_Contender &a,const FP_I09_Contender &b){ if(a.first_hunt_m1!=b.first_hunt_m1) return a.first_hunt_m1<b.first_hunt_m1?-1:1; if(a.confirmation_close!=b.confirmation_close) return a.confirmation_close<b.confirmation_close?-1:1; int ar=FP_I09_RelationRank(a.relation),br=FP_I09_RelationRank(b.relation); if(ar!=br) return ar<br?-1:1; if(a.direction!=b.direction) return a.direction<b.direction?-1:1; if(a.hunter_symbol!=b.hunter_symbol) return a.hunter_symbol<b.hunter_symbol?-1:1; return a.signal_id==b.signal_id?0:(a.signal_id<b.signal_id?-1:1); }
#endif
