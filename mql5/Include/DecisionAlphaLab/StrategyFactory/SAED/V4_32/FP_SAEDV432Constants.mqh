#ifndef FP_SAEDV432CONSTANTS_MQH
#define FP_SAEDV432CONSTANTS_MQH
// SAED_V4_32 constants and phase identity; research_only; no broker/runtime authority.
struct SAEDV432Constants
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
bool SAEDV432Validate1(const SAEDV432Constants &value)
  {
   return(value.phase=="SAED_V4_32" && value.research_only && !value.promotion_authority && !value.execution_authority && !value.live_trading_authority && value.safe_action=="quarantine");
  }
#endif
