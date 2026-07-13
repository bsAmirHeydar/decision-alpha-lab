#ifndef ALPHALAB_UCEI15_INVENTORY_MQH
#define ALPHALAB_UCEI15_INVENTORY_MQH
#include "UCEI15_Types.mqh"
bool UCEI15_IsRealData(const int mode){return(mode!=UCEI15_FIXTURE&&(mode==UCEI15_HISTORICAL_REAL||mode==UCEI15_PROSPECTIVE_PAPER));}
bool UCEI15_InventoryPass(const int row_count,const long start_ms,const long end_ms,const long cut_ms,const bool require_real,const int mode){if(row_count<1)return(false);if(start_ms>end_ms||cut_ms<end_ms)return(false);if(require_real&&!UCEI15_IsRealData(mode))return(false);return(true);}
#endif
