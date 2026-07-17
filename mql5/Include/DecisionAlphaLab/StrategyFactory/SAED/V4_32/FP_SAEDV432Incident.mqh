#ifndef FP_SAEDV432INCIDENT_MQH
#define FP_SAEDV432INCIDENT_MQH
// SAED_V4_32 incident containment; research_only; no broker/runtime authority.
struct SAEDV432Incident
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
bool SAEDV432Validate20(const SAEDV432Incident &value)
  {
   return(value.phase=="SAED_V4_32" && value.research_only && !value.promotion_authority && !value.execution_authority && !value.live_trading_authority && value.safe_action=="quarantine");
  }
#endif
