#property strict
#include <Trade/Trade.mqh>
void OnTick(){ CTrade t; ObjectCreate(0,"x",OBJ_HLINE,0,0,0); WebRequest("GET","x","",NULL,0,NULL,NULL); }
