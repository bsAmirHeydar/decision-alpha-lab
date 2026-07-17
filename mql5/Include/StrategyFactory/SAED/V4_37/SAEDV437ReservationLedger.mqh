#ifndef SAED_V4_37_RESERVATIONLEDGER_MQH
#define SAED_V4_37_RESERVATIONLEDGER_MQH
// SAED_V4_37 ReservationLedger: research-only static contract mirror.
struct SAEDV437ReservationLedger { string object_id; string object_hash; bool research_only; bool production_authorized; };
bool SAEDV437ValidateReservationLedger(const SAEDV437ReservationLedger &x){ return x.object_id!="" && x.object_hash!="" && x.research_only && !x.production_authorized; }
#endif
