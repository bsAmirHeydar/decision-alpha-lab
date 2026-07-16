#ifndef SAEDV416_COMPETING_MQH
#define SAEDV416_COMPETING_MQH
#define SAED_V4_16_PHASE "SAED_V4_16"
bool SAEDV416CompetingRiskSimplexValid(const double survival,const double &incidence[]){double total=survival;for(int i=0;i<ArraySize(incidence);i++){if(incidence[i]<0.0||incidence[i]>1.0)return false;total+=incidence[i];}return total<=1.000000000001;}
#endif
