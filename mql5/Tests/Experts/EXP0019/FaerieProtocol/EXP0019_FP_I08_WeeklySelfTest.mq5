#property strict
#include <AlphaLab/EXP0019/FaerieProtocol/I08/FP_I08_All.mqh>
int OnInit(){string reason="";if(!FP_I08_CompileWW("W1","W2",reason))return(INIT_FAILED);if(FP_I08_ResolutionPolicy()!="NEWEST_ACTIVE_CONFIRMED_WW_WINS")return(INIT_FAILED);Print("FP-I08 SELF TEST PASS");return(INIT_SUCCEEDED);}
void OnTick(){}
