#ifndef ALPHA_LAB_SAED_V4_VIEW_CATALOG_MQH
#define ALPHA_LAB_SAED_V4_VIEW_CATALOG_MQH
int SAEDInstitutionalViewCount(){ return 10; }
string SAEDViewKindName(const int kind){ string names[10]={"price","structure","time","higher_timeframe","intermarket","liquidity","session","execution","context_ancestry","treatment_descriptor"}; if(kind<0||kind>=10)return "unknown"; return names[kind]; }
#endif
