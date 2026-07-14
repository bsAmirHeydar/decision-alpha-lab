#ifndef __FP_I09_CONTRACTS_MQH__
#define __FP_I09_CONTRACTS_MQH__
#include "FP_I09_Enums.mqh"
struct FP_I09_QuotaKey { string quota_key_id,context_epoch,trading_day_id,pair_id,owner_session_id,session_kind,key_hash; };
struct FP_I09_Contender { string contender_id,signal_id,relation,direction,hunter_symbol; long first_hunt_m1,confirmation_close; string contender_hash; };
struct FP_I09_Reservation { string reservation_id,quota_key_id,winner_signal_id,winner_contender_id,prior_reservation_id,reason_code,reservation_hash; int generation; long reserved_utc; ENUM_FP_I09_RESERVATION_FINALITY finality; };
struct FP_I09_LedgerEvent { string event_id,event_type,aggregate_id,signal_id,quota_key_id,reason_code,payload_hash,prior_event_hash,event_hash; long sequence,occurred_utc; };
#endif
