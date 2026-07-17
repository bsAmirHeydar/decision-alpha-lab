#ifndef FP_SAEDV432AUTHORITY_MQH
#define FP_SAEDV432AUTHORITY_MQH
// SAED_V4_32 zero authority boundary; research_only; no broker/runtime authority.
struct SAEDV432Authority
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
bool SAEDV432Validate2(const SAEDV432Authority &value)
  {
   return(value.phase=="SAED_V4_32" && value.research_only && !value.promotion_authority && !value.execution_authority && !value.live_trading_authority && value.safe_action=="quarantine");
  }
#endif
