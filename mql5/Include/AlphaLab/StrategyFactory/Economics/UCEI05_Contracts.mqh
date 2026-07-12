#ifndef UCEI05_CONTRACTS_MQH
#define UCEI05_CONTRACTS_MQH
#include "UCEI05_Enums.mqh"
struct UCEI05_QuoteSnapshot { string symbol; double bid; double ask; long source_time_ms; long known_time_ms; long sequence; };
struct UCEI05_SymbolSpec { string symbol; int digits; double point; double tick_size; double tick_value_profit; double tick_value_loss; double contract_size; double volume_min; double volume_max; double volume_step; int stops_level_points; int freeze_level_points; double leverage; double margin_per_lot; long known_time_ms; string definition_id; };
struct UCEI05_AccountSnapshot { string account_id; string currency; double balance; double equity; double free_margin; double peak_equity; double daily_loss; double open_risk; double reserved_risk; long known_time_ms; };
struct UCEI05_CostProfile { string definition_id; double commission_per_lot_per_side; double minimum_commission; double entry_slippage_points_long; double entry_slippage_points_short; double exit_slippage_points_long; double exit_slippage_points_short; double gap_reserve_points; double reserve_multiplier; int max_quote_age_ms; long max_spec_age_ms; };
struct UCEI05_RiskGeometry { string treatment_id; int side; int order_kind; double logical_entry; double logical_stop; double logical_target; bool has_target; int entry_transactions; int exit_transactions; double holding_days; double volatility_points; };
struct UCEI05_CostBreakdown { double spread_cash; double entry_slippage_cash; double exit_slippage_cash; double commission_cash; double financing_cash; double tax_cash; double conversion_cash; double gap_reserve_cash; double total_cash; };
struct UCEI05_CapitalBudget { string budget_id; double requested_cash; double approved_cash; bool accepted; string reason_code; };
struct UCEI05_EconomicEnvelope { string treatment_id; string economics_id; int side; double entry_exec; double stop_exec; double target_exec; bool has_target; double raw_volume; double volume; double price_loss_cash; UCEI05_CostBreakdown costs; double maximum_loss_cash; double target_gross_cash; double target_net_cash; double margin_required; double risk_budget_cash; bool accepted; string reason_code; };
struct UCEI05_ReservationRecord { string reservation_id; string treatment_id; string account_id; double reserved_cash; double consumed_cash; double released_cash; int state; long last_sequence; string last_hash; };
#endif
