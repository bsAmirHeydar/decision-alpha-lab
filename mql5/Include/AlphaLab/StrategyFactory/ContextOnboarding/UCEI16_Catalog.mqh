#ifndef ALPHALAB_UCEI16_CATALOG_MQH
#define ALPHALAB_UCEI16_CATALOG_MQH
int UCEI16_WaveACount(){ return 2; }
int UCEI16_WaveBCount(){ return 6; }
int UCEI16_WaveCCount(){ return 4; }
int UCEI16_TotalMigrationUnitCount(){ return UCEI16_WaveACount()+UCEI16_WaveBCount()+UCEI16_WaveCCount(); }
string UCEI16_ContextAt(const int index){ string ids[12]={"temporal_intermarket_divergence","exp0017_family","nds","hook","f_counting","rally","zone","structural_nodes","daye_cycle","ict_deterministic","astro_features","manual_only_setups"}; if(index<0 || index>=12) return ""; return ids[index]; }
#endif
