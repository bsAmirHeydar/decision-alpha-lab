#property strict
#include <AlphaLab/StrategyFactory/ClassicalAlgorithms/UCEI08_All.mqh>
int OnInit(){CUCEI08_Registry r;UCEI08_RegisterCatalog(r);Print("UCE-I08 classical catalog size=",r.Size()," frozen=",r.Frozen());return r.Size()>=20 && r.Frozen()?INIT_SUCCEEDED:INIT_FAILED;}
void OnTick(){}
