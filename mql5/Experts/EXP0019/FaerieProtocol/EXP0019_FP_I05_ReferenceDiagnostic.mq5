#property strict
#include <AlphaLab/EXP0019/FaerieProtocol/I05/FP_I05_All.mqh>
int OnInit(){ Print("FP-I05 Reference Diagnostic | version=",FP_I05_Registry::Version()," | contracts=",FP_I05_Registry::ContractCount()," | authority=",FP_I05_Registry::Authority()); return INIT_SUCCEEDED; }
void OnTick(){}
