
#ifndef __EXP0018_DAYE_PERIOD_SELF_TEST_MQH__
#define __EXP0018_DAYE_PERIOD_SELF_TEST_MQH__

#include <DayeTrader/EXP0018/DAYE_PeriodAudit.mqh>

void DAYE_P03BuildSyntheticSymbolBar(const string canonical,
                                     const datetime event_utc,
                                     const int base_seconds,
                                     const double price,
                                     DAYE_SymbolBar &bar)
{
   ZeroMemory(bar);
   bar.schema_version = DAYE_DATA_SCHEMA_VERSION;
   bar.status = DAYE_DATA_STATUS_OK;
   bar.reason_code = "synthetic_test";
   bar.is_valid = true;
   bar.broker_symbol = canonical + "_BROKER";
   bar.canonical_symbol = canonical;
   bar.timeframe = PERIOD_M1;
   bar.event_time_utc = event_utc;
   bar.event_time_ny = event_utc;
   bar.close_time_utc = event_utc + base_seconds;
   bar.open = price;
   bar.high = price + 1.0;
   bar.low = price - 1.0;
   bar.close = price + 0.25;
   bar.tick_volume = 1;
   bar.real_volume = 1;
   bar.spread = 1;
   bar.completeness = DAYE_BAR_COMPLETENESS_CLOSED;
   bar.is_replay_safe = true;
}

bool DAYE_P03SelfTestCompleteP4(void)
{
   DAYE_PeriodAggregationConfig config;
   ZeroMemory(config);
   config.include_open_periods = true;
   config.publish_partial_periods = true;
   config.minimum_publishable_coverage_percent = 0.0;

   DAYE_PeriodWindow window;
   ZeroMemory(window);
   window.period_id = DAYE_PERIOD_P4;
   window.family = DAYE_FAMILY_SUBCYCLE_TAIL;
   window.code = "p4";
   window.instance_id = "TEST|P4";
   window.start_utc = D'2026.01.05 16:30:00';
   window.end_utc = D'2026.01.05 17:00:00';

   DAYE_SymbolPeriodSnapshot items[];
   ArrayResize(items,0);
   for(int i=0;i<30;i++)
   {
      DAYE_SymbolBar bar;
      DAYE_P03BuildSyntheticSymbolBar("SPX",window.start_utc+i*60,60,100.0+i,bar);
      if(!DAYE_AccumulateBarIntoPeriod(bar,window,"2026-01-04",60,window.end_utc,items)) return false;
   }
   if(ArraySize(items) != 1) return false;
   DAYE_FinalizeSymbolPeriodSnapshot(items[0],window.end_utc,config);
   return (items[0].expected_bar_count == 30 && items[0].observed_bar_count == 30 && items[0].completeness == DAYE_PERIOD_COMPLETENESS_COMPLETE);
}

bool DAYE_P03SelfTestPartialClosedPeriod(void)
{
   DAYE_PeriodAggregationConfig config;
   ZeroMemory(config);
   config.publish_partial_periods = true;
   config.minimum_publishable_coverage_percent = 0.0;
   DAYE_SymbolPeriodSnapshot s;
   ZeroMemory(s);
   s.base_bar_seconds = 60;
   s.window.start_utc = D'2026.01.05 16:30:00';
   s.window.end_utc = D'2026.01.05 17:00:00';
   s.observed_bar_count = 10;
   s.first_source_bar_utc = s.window.start_utc;
   s.last_source_bar_utc = s.window.start_utc + 9*60;
   DAYE_FinalizeSymbolPeriodSnapshot(s,s.window.end_utc,config);
   return (s.completeness == DAYE_PERIOD_COMPLETENESS_PARTIAL && s.missing_bar_count == 20);
}

bool DAYE_P03SelfTestOpenPeriod(void)
{
   DAYE_PeriodAggregationConfig config;
   ZeroMemory(config);
   config.include_open_periods = true;
   config.minimum_publishable_coverage_percent = 0.0;
   DAYE_SymbolPeriodSnapshot s;
   ZeroMemory(s);
   s.base_bar_seconds = 60;
   s.window.start_utc = D'2026.01.05 16:30:00';
   s.window.end_utc = D'2026.01.05 17:00:00';
   s.observed_bar_count = 10;
   s.first_source_bar_utc = s.window.start_utc;
   s.last_source_bar_utc = s.window.start_utc + 9*60;
   DAYE_FinalizeSymbolPeriodSnapshot(s,s.window.start_utc+10*60,config);
   return (s.completeness == DAYE_PERIOD_COMPLETENESS_OPEN && s.is_publishable);
}

bool DAYE_P03SelfTestNoDataIsUnavailable(void)
{
   DAYE_PeriodAggregationConfig config;
   ZeroMemory(config);
   DAYE_SymbolPeriodSnapshot s;
   ZeroMemory(s);
   s.base_bar_seconds = 60;
   s.window.start_utc = D'2026.01.05 16:30:00';
   s.window.end_utc = D'2026.01.05 17:00:00';
   DAYE_FinalizeSymbolPeriodSnapshot(s,s.window.end_utc,config);
   return (s.completeness == DAYE_PERIOD_COMPLETENESS_EMPTY && s.completeness != DAYE_PERIOD_COMPLETENESS_COMPLETE);
}

bool DAYE_RunEmbeddedPeriodAggregationSelfTests(void)
{
   bool ok = true;
   if(!DAYE_P03SelfTestCompleteP4()) { Print("EXP0018 P03 self-test failed: complete p4"); ok=false; }
   if(!DAYE_P03SelfTestPartialClosedPeriod()) { Print("EXP0018 P03 self-test failed: partial closed period"); ok=false; }
   if(!DAYE_P03SelfTestOpenPeriod()) { Print("EXP0018 P03 self-test failed: open period"); ok=false; }
   if(!DAYE_P03SelfTestNoDataIsUnavailable()) { Print("EXP0018 P03 self-test failed: empty period"); ok=false; }
   if(ok) Print("EXP0018 P03 embedded period aggregation self-tests: PASS");
   return ok;
}

#endif
