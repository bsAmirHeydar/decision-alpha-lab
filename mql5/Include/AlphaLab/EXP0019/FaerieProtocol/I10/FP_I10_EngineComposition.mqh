#ifndef __FP_I10_ENGINE_COMPOSITION_MQH__
#define __FP_I10_ENGINE_COMPOSITION_MQH__
#include <FaerieProtocol/EXP0019/Time/FP_I03_All.mqh>
#include <FaerieProtocol/EXP0019/Data/FP_I04_All.mqh>
#include <AlphaLab/EXP0019/FaerieProtocol/I05/FP_I05_All.mqh>
#include <AlphaLab/EXP0019/FaerieProtocol/I06/FP_I06_All.mqh>
#include <AlphaLab/EXP0019/FaerieProtocol/I07/FP_I07_All.mqh>
#include <AlphaLab/EXP0019/FaerieProtocol/I08/FP_I08_All.mqh>
#include <AlphaLab/EXP0019/FaerieProtocol/I09/FP_I09_All.mqh>
#include "FP_I10_Contracts.mqh"
bool FP_I10_ValidateComposition(string &reason){
 if(FP_I04_VERSION!="1.0.0"){reason="FP_IND_I04_VERSION_MISMATCH";return false;}
 if(FP_I05_Registry::Version()!="1.0.0"){reason="FP_IND_I05_VERSION_MISMATCH";return false;}
 if(FP_I06_Registry::Version()!="1.0.0"){reason="FP_IND_I06_VERSION_MISMATCH";return false;}
 if(FP_I07_ModuleVersion()!="1.0.0"){reason="FP_IND_I07_VERSION_MISMATCH";return false;}
 if(FP_I08_Version()!="1.0.0"){reason="FP_IND_I08_VERSION_MISMATCH";return false;}
 if(FP_I09_PHASE_VERSION!="1.0.0"){reason="FP_IND_I09_VERSION_MISMATCH";return false;}
 if(FP_I09_CONSUMPTION_POLICY!="UNSET"){reason="FP_IND_I09_CONSUMPTION_POLICY_CHANGED";return false;}
 reason="FP_IND_UPSTREAM_VALIDATED"; return true;
}
#endif
