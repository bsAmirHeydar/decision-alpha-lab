#property strict
#include <AlphaLab/EXP0019/FaerieProtocol/I08/FP_I08_All.mqh>
int OnInit(){Print("FP-I08 Weekly Diagnostic ",FP_I08_Version()," policy=",FP_I08_ResolutionPolicy());return(INIT_SUCCEEDED);}
void OnTick(){}
