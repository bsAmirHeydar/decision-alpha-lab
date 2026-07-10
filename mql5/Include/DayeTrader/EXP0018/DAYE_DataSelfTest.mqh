
#ifndef __EXP0018_DAYE_DATA_SELF_TEST_MQH__
#define __EXP0018_DAYE_DATA_SELF_TEST_MQH__

#include <DayeTrader/EXP0018/DAYE_DataSynchronizer.mqh>

void DAYE_TestBuildBar(const string broker_symbol,const string canonical_symbol,const datetime event_utc,const double base,DAYE_SymbolBar &bar)
{
   ZeroMemory(bar);
   bar.schema_version = DAYE_DATA_SCHEMA_VERSION;
   bar.status = DAYE_DATA_STATUS_OK;
   bar.reason_code = "fixture";
   bar.is_valid = true;
   bar.broker_symbol = broker_symbol;
   bar.canonical_symbol = canonical_symbol;
   bar.timeframe = PERIOD_M1;
   bar.event_time_utc = event_utc;
   bar.event_time_ny = event_utc;
   bar.close_time_utc = event_utc + 60;
   bar.open = base;
   bar.high = base + 2.0;
   bar.low = base - 2.0;
   bar.close = base + 1.0;
   bar.completeness = DAYE_BAR_COMPLETENESS_CLOSED;
   bar.is_replay_safe = true;
}

bool DAYE_TestExactAlignment(void)
{
   DAYE_SymbolBar a[];
   DAYE_SymbolBar b[];
   ArrayResize(a,3);
   ArrayResize(b,3);
   for(int i=0;i<3;i++)
   {
      DAYE_TestBuildBar("A","A",1000 + i*60,100.0+i,a[i]);
      DAYE_TestBuildBar("B","B",1000 + i*60,200.0+i,b[i]);
   }
   DAYE_DataSyncConfig cfg;
   ZeroMemory(cfg);
   cfg.schema_version = DAYE_DATA_SCHEMA_VERSION;
   cfg.base_timeframe = PERIOD_M1;
   cfg.canonical_symbol_a = "A";
   cfg.canonical_symbol_b = "B";
   cfg.minimum_common_bars = 1;
   cfg.maximum_pairs_to_publish = 10;
   DAYE_SynchronizedBarPair pairs[];
   DAYE_DataSyncSummary summary;
   ZeroMemory(summary);
   bool ok = DAYE_AlignBarsByExactUtc(a,b,cfg,2000,pairs,summary);
   return (ok && summary.aligned_count == 3 && summary.unmatched_a == 0 && summary.unmatched_b == 0 && pairs[1].symbol_a.open == 101.0 && pairs[1].symbol_b.open == 201.0);
}

bool DAYE_TestMissingBarIsExplicit(void)
{
   DAYE_SymbolBar a[];
   DAYE_SymbolBar b[];
   ArrayResize(a,3);
   ArrayResize(b,2);
   DAYE_TestBuildBar("A","A",1000,100.0,a[0]);
   DAYE_TestBuildBar("A","A",1060,101.0,a[1]);
   DAYE_TestBuildBar("A","A",1120,102.0,a[2]);
   DAYE_TestBuildBar("B","B",1000,200.0,b[0]);
   DAYE_TestBuildBar("B","B",1120,202.0,b[1]);
   DAYE_DataSyncConfig cfg;
   ZeroMemory(cfg);
   cfg.schema_version = DAYE_DATA_SCHEMA_VERSION;
   cfg.base_timeframe = PERIOD_M1;
   cfg.canonical_symbol_a = "A";
   cfg.canonical_symbol_b = "B";
   cfg.minimum_common_bars = 1;
   cfg.maximum_pairs_to_publish = 10;
   cfg.require_complete_alignment = false;
   DAYE_SynchronizedBarPair pairs[];
   DAYE_DataSyncSummary summary;
   ZeroMemory(summary);
   bool ok = DAYE_AlignBarsByExactUtc(a,b,cfg,2000,pairs,summary);
   return (ok && summary.aligned_count == 2 && summary.unmatched_a == 1 && summary.unmatched_b == 0 && pairs[0].event_time_utc == 1000 && pairs[1].event_time_utc == 1120);
}

bool DAYE_TestShiftedIndicesDoNotAlign(void)
{
   DAYE_SymbolBar a[];
   DAYE_SymbolBar b[];
   ArrayResize(a,2);
   ArrayResize(b,2);
   DAYE_TestBuildBar("A","A",1000,100.0,a[0]);
   DAYE_TestBuildBar("A","A",1060,101.0,a[1]);
   DAYE_TestBuildBar("B","B",1001,200.0,b[0]);
   DAYE_TestBuildBar("B","B",1061,201.0,b[1]);
   DAYE_DataSyncConfig cfg;
   ZeroMemory(cfg);
   cfg.schema_version = DAYE_DATA_SCHEMA_VERSION;
   cfg.base_timeframe = PERIOD_M1;
   cfg.canonical_symbol_a = "A";
   cfg.canonical_symbol_b = "B";
   cfg.minimum_common_bars = 1;
   cfg.maximum_pairs_to_publish = 10;
   DAYE_SynchronizedBarPair pairs[];
   DAYE_DataSyncSummary summary;
   ZeroMemory(summary);
   bool ok = DAYE_AlignBarsByExactUtc(a,b,cfg,2000,pairs,summary);
   return (!ok && summary.status == DAYE_DATA_STATUS_NO_COMMON_TIMESTAMPS && ArraySize(pairs) == 0);
}

bool DAYE_TestPairIdentityDeterministic(void)
{
   DAYE_DataSyncConfig cfg;
   ZeroMemory(cfg);
   cfg.base_timeframe = PERIOD_M1;
   cfg.canonical_symbol_a = "SPX";
   cfg.canonical_symbol_b = "NDX";
   string a = DAYE_BuildSynchronizedPairId(cfg,123456);
   string b = DAYE_BuildSynchronizedPairId(cfg,123456);
   return (a == b && StringFind(a,"123456") >= 0);
}

bool DAYE_RunEmbeddedDataSyncSelfTests(void)
{
   bool pass = true;
   if(!DAYE_TestExactAlignment())
   {
      Print("EXP0018 P02 self-test failed: exact alignment");
      pass = false;
   }
   if(!DAYE_TestMissingBarIsExplicit())
   {
      Print("EXP0018 P02 self-test failed: missing bar explicitness");
      pass = false;
   }
   if(!DAYE_TestShiftedIndicesDoNotAlign())
   {
      Print("EXP0018 P02 self-test failed: timestamp vs index alignment");
      pass = false;
   }
   if(!DAYE_TestPairIdentityDeterministic())
   {
      Print("EXP0018 P02 self-test failed: deterministic pair identity");
      pass = false;
   }
   if(pass)
      Print("EXP0018 P02 embedded data-sync self-tests: PASS");
   return pass;
}

#endif
