#property strict
#include <AlphaLab/EXP0019/FaerieProtocol/I06/FP_I06_All.mqh>
int OnInit(){Print("FP-I06 diagnostic relation_count=",FP_I06_RelationRegistry::RelationCount()," supported=",FP_I06_RelationRegistry::SupportedCount()," authority=",FP_I06_Registry::RuntimeAuthority());return INIT_SUCCEEDED;}
void OnTick(){}
