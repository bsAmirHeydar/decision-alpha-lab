#ifndef __SF20_EXP0017_FIXTURE_MQH__
#define __SF20_EXP0017_FIXTURE_MQH__
#include "../SF20_EXP0017Mapper.mqh"
void SF20_BuildReferenceLegacyCandidate(const bool buy,SCGDDivergenceCandidate &c)
{
 c.divergence_id=buy?"EXP0017_ref_buy":"EXP0017_ref_sell";c.group_name=buy?"cg_15m":"cg_60m";c.group_minutes=buy?15:60;c.current_cycle_index=4;c.current_cycle_number=5;c.reference_cycle_index=3;c.reference_cycle_number=4;c.trading_day_start_ny=(datetime)1783771200;c.trading_day_end_ny=(datetime)1783857600;c.current_cycle_start_ny=(datetime)(buy?1783792800:1783794000);c.current_cycle_end_ny=(datetime)(buy?1783793700:1783797600);c.reference_cycle_start_ny=(datetime)(buy?1783791900:1783790400);c.reference_cycle_end_ny=c.current_cycle_start_ny;c.direction=buy?CGD_DIRECTION_BUY:CGD_DIRECTION_SELL;c.side=buy?CGD_SIDE_LOW:CGD_SIDE_HIGH;c.status=CGD_STATUS_CANDIDATE;c.hunter_symbol=buy?"SPXUSD":"NDXUSD";c.clean_symbol=buy?"NDXUSD":"SPXUSD";c.non_hunter_symbol=c.clean_symbol;c.symbol_a_is_hunter=buy;c.symbol_b_is_hunter=!buy;c.one_sided_hunt=true;c.both_symbols_hunted_same_side=false;c.data_ready=true;c.hunter_reference_price=buy?6240.0:22500.0;c.clean_reference_price=buy?22400.0:6260.0;c.hunter_current_extreme=buy?6238.0:22508.0;c.clean_current_extreme=buy?22402.0:6258.0;c.clean_stop_reference_price=c.clean_reference_price;c.note="phase20_reference_fixture";
}
#endif
