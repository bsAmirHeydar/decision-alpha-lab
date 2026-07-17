#ifndef __SAEDV441_QUARANTINE_MQH__
#define __SAEDV441_QUARANTINE_MQH__
// SAEDV441 static parity mirror: Quarantine
#define SAEDV441_PHASE_ID "SAED_V4_41"
#define SAEDV441_LIVE_ORDER_SUBMISSION_ALLOWED 0
#define SAEDV441_CAPITAL_ACTIVATION_ALLOWED 0
#define SAEDV441_PRODUCTION_AUTHORIZED 0
#define SAEDV441_REINSTATEMENT_WITHOUT_REQUALIFICATION_ALLOWED 0
#define SAEDV441_CROSS_TENANT_ACTION_ALLOWED 0
struct SAEDV441QuarantineRecord
{
   string record_id;
   string cell_id;
   string tenant_id;
   string known_time;
   string content_hash;
   bool   research_only;
   bool   live_side_effect_allowed;
};
bool SAEDV441ValidateQuarantine(const SAEDV441QuarantineRecord &value)
{
   if(value.record_id=="" || value.content_hash=="") return false;
   if(!value.research_only || value.live_side_effect_allowed) return false;
   return true;
}
#endif
