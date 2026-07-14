#ifndef FP_I15_CONTRACTS_MQH
#define FP_I15_CONTRACTS_MQH
#include "FP_I15_Enums.mqh"
struct FP_I15_QuoteSnapshot { string quote_id; string symbol; double bid; double ask; datetime captured_at; string source_revision_id; };
struct FP_I15_SymbolSpec { string symbol; double tick_size; double tick_value_loss; double volume_min; double volume_max; double volume_step; double stops_level_price; double freeze_level_price; };
struct FP_I15_RiskConfig { double fixed_risk_amount; double target_r_multiple; double max_slippage_price; double round_trip_cost_per_lot; };
struct FP_I15_WinnerInput { string signal_id; string signal_hash; string protected_symbol; string quota_key_id; string i09_reservation_id; FP_I15_DIRECTION direction; double raw_structural_stop; datetime confirmation_close; string config_hash; string source_revision_id; };
struct FP_I15_Geometry { FP_I15_GEOMETRY_STATUS status; double entry; double worst_entry; double raw_stop; double spread; double adjusted_stop; double target; double stop_distance; string reason_code; };
struct FP_I15_Sizing { FP_I15_GEOMETRY_STATUS status; double loss_per_lot; double raw_volume; double volume; double max_loss; string reason_code; };
struct FP_I15_Plan { string plan_id; string signal_id; string quota_key_id; string trade_symbol; FP_I15_DIRECTION direction; FP_I15_Geometry geometry; FP_I15_Sizing sizing; string reason_code; };
struct FP_I15_QuotaRecord { string quota_key_id; FP_I15_QUOTA_STATE state; string winner_signal_id; string plan_id; string reservation_id; FP_I15_CONSUME_EVENT consumed_event; int generation; };
struct FP_I15_PaperOrder { string order_id; string plan_id; FP_I15_ORDER_STATE state; double requested_volume; double filled_volume; double average_fill_price; string reason_code; };
#endif
