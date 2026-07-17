#ifndef FP_SAEDV432CAPABILITY_MQH
#define FP_SAEDV432CAPABILITY_MQH
// SAED_V4_32 deny by default capability; research_only; no broker/runtime authority.
struct SAEDV432Capability
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
bool SAEDV432Validate5(const SAEDV432Capability &value)
  {
   return(value.phase=="SAED_V4_32" && value.research_only && !value.promotion_authority && !value.execution_authority && !value.live_trading_authority && value.safe_action=="quarantine");
  }
#endif
