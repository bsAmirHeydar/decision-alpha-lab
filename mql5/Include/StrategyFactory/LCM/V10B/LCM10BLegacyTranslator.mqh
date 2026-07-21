#ifndef __LCM10B_LEGACY_TRANSLATOR_MQH__
#define __LCM10B_LEGACY_TRANSLATOR_MQH__
#include "LCM10BTypes.mqh"
class CLCM10BLegacyTranslator { public: bool TranslateExplicit(const string decision_id,const string symbol,const ENUM_LCM10B_SIDE side,const ENUM_LCM10B_ENTRY_KIND kind,const datetime decision_time,const datetime availability_time,LCM10BExecutionIntent &out,string &reason){ if(decision_id==""||symbol==""||side==LCM10B_SIDE_UNKNOWN||kind==LCM10B_ENTRY_UNSPECIFIED){reason="EXPLICIT_FIELDS_REQUIRED";return false;} out.intent_id=decision_id;out.symbol=symbol;out.side=side;out.entry_kind=kind;out.decision_time=decision_time;out.availability_time=availability_time;out.submission_requested=false;reason="REFERENCE_TRANSLATED";return true;} };
#endif
