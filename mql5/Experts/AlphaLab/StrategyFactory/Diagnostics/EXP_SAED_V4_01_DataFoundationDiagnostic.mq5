#property strict
#include <AlphaLab/StrategyFactory/SAEDV4DataFoundation/DataFoundationAll.mqh>
int OnInit(){
 Print("SAED V4-01 Data Foundation diagnostic version=",AL_SAED_V4_DATA_FOUNDATION_VERSION,
       " order_authority=",AL_SAED_V4_DATA_ORDER_AUTHORITY,
       " broker_authority=",AL_SAED_V4_DATA_BROKER_AUTHORITY,
       " network_authority=",AL_SAED_V4_DATA_NETWORK_AUTHORITY);
 return(INIT_SUCCEEDED);
}
void OnTick(){}
