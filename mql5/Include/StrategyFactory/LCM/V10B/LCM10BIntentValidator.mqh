#ifndef __LCM10B_INTENT_VALIDATOR_MQH__
#define __LCM10B_INTENT_VALIDATOR_MQH__
#include "LCM10BTypes.mqh"
class CLCM10BIntentValidator { public: bool Validate(const LCM10BExecutionIntent &intent,string &reason) const { if(intent.submission_requested){reason="SUBMISSION_MUST_BE_FALSE";return false;} if(intent.symbol==""){reason="SYMBOL_REQUIRED";return false;} if(intent.side==LCM10B_SIDE_UNKNOWN){reason="SIDE_REQUIRED";return false;} if(intent.entry_kind==LCM10B_ENTRY_UNSPECIFIED){reason="ENTRY_KIND_REQUIRED";return false;} reason="PASS";return true;} };
#endif
