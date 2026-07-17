#ifndef FP_SAEDV432TASKENVELOPE_MQH
#define FP_SAEDV432TASKENVELOPE_MQH
// SAED_V4_32 typed task envelope; research_only; no broker/runtime authority.
struct SAEDV432TaskEnvelope
  {
   string phase;
   string identity;
   string content_hash;
   bool research_only;
   bool promotion_authority;
   bool execution_authority;
   bool live_trading_authority;
   string safe_action;
  };
bool SAEDV432Validate7(const SAEDV432TaskEnvelope &value)
  {
   return(value.phase=="SAED_V4_32" && value.research_only && !value.promotion_authority && !value.execution_authority && !value.live_trading_authority && value.safe_action=="quarantine");
  }
#endif
