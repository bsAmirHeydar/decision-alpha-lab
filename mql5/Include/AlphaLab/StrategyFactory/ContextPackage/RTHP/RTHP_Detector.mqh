#ifndef ALPHA_LAB_RTHP_DETECTOR_MQH
#define ALPHA_LAB_RTHP_DETECTOR_MQH
#include "RTHP_Types.mqh"
bool RTHP_Evaluate(const ENUM_RTHP_LEVEL_SIDE side,const string basis_a,const string basis_b,const int available_refs,const RTHP_SymbolObservation &a,const RTHP_SymbolObservation &b,RTHP_Evaluation &out){out.event_created=false;out.polarity="";out.hunter_symbol="";out.protected_symbol="";if(available_refs<1){out.status=RTHP_EVAL_INSUFFICIENT_HISTORY;return true;}if(basis_a!=basis_b){out.status=RTHP_EVAL_INVALID_BASIS;return true;}if(a.data_status!=RTHP_DATA_VALID||b.data_status!=RTHP_DATA_VALID){out.status=RTHP_EVAL_UNCONFIRMED;return true;}if(a.touched==b.touched){out.status=RTHP_EVAL_NO_EVENT;return true;}out.status=RTHP_EVAL_CONFIRMED;out.event_created=true;out.polarity=(side==RTHP_LEVEL_HIGH?"BEARISH_DIVERGENCE":"BULLISH_DIVERGENCE");out.hunter_symbol=(a.touched?a.symbol:b.symbol);out.protected_symbol=(a.touched?b.symbol:a.symbol);return true;}
#endif
