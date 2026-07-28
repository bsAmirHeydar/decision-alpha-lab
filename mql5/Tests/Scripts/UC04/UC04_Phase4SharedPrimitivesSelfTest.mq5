//+------------------------------------------------------------------+
//| Decision Alpha Lab — UC-04 shared-primitives native self-test    |
//| No order, position, network, credential, or capital authority.   |
//+------------------------------------------------------------------+
#property strict
#property script_show_inputs

#include <AlphaLab/UC04/AL_UC04CorePrimitives.mqh>
#include <AlphaLab/UC04/AL_UC04MarketStream.mqh>
#include <AlphaLab/UC04/AL_UC04M0001Config.mqh>
#include <AlphaLab/UC04/AL_UC04M0002Config.mqh>
#include <AlphaLab/UC04/AL_UC04DayeTimeConfig.mqh>

#define UC04_TEST_OUTPUT "AlphaLab\\UC04\\UC04_Phase4SharedPrimitivesSelfTest.csv"
#define UC04_TEST_PREFIX "AL_UC04_SELFTEST_"

int g_uc04_passed = 0;
int g_uc04_failed = 0;
int g_uc04_handle = INVALID_HANDLE;

void UC04_Record(const string test_id, const bool passed, const string detail)
{
   if(passed)
      g_uc04_passed++;
   else
      g_uc04_failed++;

   Print("UC04_SELFTEST|", test_id, "|", (passed ? "PASS" : "FAIL"), "|", detail);
   if(g_uc04_handle != INVALID_HANDLE)
      FileWrite(g_uc04_handle, test_id, (passed ? "PASS" : "FAIL"), detail);
}

bool UC04_DoubleEqual(const double a, const double b)
{
   return (MathAbs(a - b) <= 0.000000000001);
}

void UC04_TestTimeframe(void)
{
   UC04_Record(
      "TIMEFRAME_CURRENT",
      AL_UC04ResolveTimeframe(PERIOD_CURRENT, PERIOD_M15) == PERIOD_M15,
      "PERIOD_CURRENT resolves to supplied current period"
   );
   UC04_Record(
      "TIMEFRAME_EXPLICIT",
      AL_UC04ResolveTimeframe(PERIOD_H1, PERIOD_M15) == PERIOD_H1,
      "explicit timeframe is preserved"
   );
}

void UC04_TestDateTime(void)
{
   datetime t = StringToTime("2026.07.28 13:45:09");
   UC04_Record(
      "DATETIME_FORMAT",
      AL_UC04FormatDateTime(t) == "2026.07.28 13:45:09",
      AL_UC04FormatDateTime(t)
   );
}

void UC04_TestClosedBarClock(void)
{
   datetime last = 0;
   bool first = AL_UC04AdvanceClosedBarClock(100, last);
   bool first_state = (last == 100);
   bool same = AL_UC04AdvanceClosedBarClock(100, last);
   bool same_state = (last == 100);
   bool next = AL_UC04AdvanceClosedBarClock(200, last);
   bool next_state = (last == 200);
   bool invalid = AL_UC04AdvanceClosedBarClock(0, last);
   bool invalid_state = (last == 200);

   UC04_Record("CLOSED_BAR_FIRST", !first && first_state, "first observation is initialization-only");
   UC04_Record("CLOSED_BAR_SAME", !same && same_state, "same open-bar time does not emit or mutate state");
   UC04_Record("CLOSED_BAR_NEXT", next && next_state, "new open-bar time confirms one closed bar");
   UC04_Record("CLOSED_BAR_INVALID", !invalid && invalid_state, "invalid time fails closed without state mutation");
}

void UC04_TestConfigurationGates(void)
{
   UC04_Record("SHOULD_RUN_DISABLED", !AL_UC04ShouldRun(false, 0, 1), "disabled fails closed");
   UC04_Record("SHOULD_RUN_RALLY_ONLY", !AL_UC04ShouldRun(true, 1, 1), "rally-only display is excluded");
   UC04_Record("SHOULD_RUN_ACTIVE", AL_UC04ShouldRun(true, 2, 1), "eligible configuration passes");
   UC04_Record("DIRECTION_POSITIVE", AL_UC04DirectionAllowed(true, false, 1, 1, -1), "positive direction");
   UC04_Record("DIRECTION_NEGATIVE", AL_UC04DirectionAllowed(false, true, -1, 1, -1), "negative direction");
   UC04_Record("DIRECTION_UNKNOWN", !AL_UC04DirectionAllowed(true, true, 0, 1, -1), "unknown direction fails closed");
}

void UC04_TestM0001Config(void)
{
   DALM0001Config cfg;
   AL_UC04BuildM0001Config(cfg, 7, 0.82, 4, DAL_M0001_CONSUME_BY_TOUCH);
   bool ok = (
      cfg.L == 7 &&
      UC04_DoubleEqual(cfg.zone_ratio, 0.82) &&
      cfg.exit_gap == 4 &&
      cfg.consume_mode == DAL_M0001_CONSUME_BY_TOUCH &&
      cfg.consume_on_touch &&
      cfg.max_events == 0 &&
      UC04_DoubleEqual(cfg.min_rtv, 0.0)
   );
   UC04_Record("M0001_CONFIG", ok, "canonical M0001 configuration assignment");
}

void UC04_TestM0002Config(void)
{
   DALM0002Config cfg;
   AL_UC04BuildM0002Config(cfg, -4, 3, 0, DAL_M0001_CONSUME_BY_HUNT);
   bool ok = (
      cfg.measure_mode == DAL_M0002_MEASURE_EVENT_RTV &&
      cfg.outcome_candle_offset_after_exit == 0 &&
      cfg.post_outcome_sample_bars == 0 &&
      !cfg.use_event_length_for_sample &&
      cfg.random_samples_per_event == 1 &&
      cfg.bootstrap_iterations == 0 &&
      cfg.permutation_iterations == 0 &&
      cfg.validation_splits == 1 &&
      cfg.broker_utc_offset_hours == 3 &&
      cfg.regime_lookback_bars == 1 &&
      !cfg.print_group_session_regime &&
      !cfg.run_stress_suite &&
      cfg.hard_random_candidates == 1 &&
      cfg.placebo_shift_bars == 1 &&
      cfg.nonoverlap_gap_bars == 0 &&
      cfg.block_bootstrap_iterations == 0 &&
      cfg.block_bootstrap_block_pairs == 1 &&
      cfg.consume_mode == DAL_M0001_CONSUME_BY_HUNT &&
      !cfg.consume_on_touch
   );
   UC04_Record("M0002_CONFIG", ok, "canonical M0002 configuration assignment");
}

void UC04_TestDayeTimeConfig(void)
{
   DAYE_TimeConfig cfg;
   AL_UC04BuildDayeTimeConfig(
      cfg,
      (DAYE_BrokerOffsetMode)0,
      3.5,
      (DAYE_NyOffsetMode)0,
      -4.0,
      (DAYE_LocalResolutionPolicy)0,
      (DAYE_LocalResolutionPolicy)0
   );
   bool ok = (
      cfg.schema_version == DAYE_TIME_SCHEMA_VERSION &&
      cfg.broker_utc_offset_minutes == 210 &&
      cfg.manual_new_york_utc_offset_minutes == -240
   );
   UC04_Record("DAYE_TIME_CONFIG", ok, "hour offsets are preserved as rounded minutes");
}

void UC04_TestFileLifecycle(void)
{
   string path = "AlphaLab\\UC04\\UC04_Phase4SharedPrimitivesLine.txt";
   int handle = FileOpen(path, FILE_WRITE | FILE_TXT | FILE_ANSI | FILE_COMMON);
   bool enabled = (handle != INVALID_HANDLE);
   bool wrote = AL_UC04WriteLine(handle, "alpha");
   AL_UC04CloseFileHandle(handle, enabled);
   UC04_Record("FILE_WRITE_LINE", wrote, "line writer accepts valid handle");
   UC04_Record("FILE_CLOSE", handle == INVALID_HANDLE && !enabled, "handle and enable state are closed deterministically");
   FileDelete(path, FILE_COMMON);
}

void UC04_TestPriceTolerance(void)
{
   double point = SymbolInfoDouble(_Symbol, SYMBOL_POINT);
   if(point <= 0.0)
      point = 0.00000001;
   UC04_Record("PRICE_TOLERANCE_PASS", AL_UC04PricesCloseEnough(_Symbol, 1.0, 1.0 + point * 0.5), "half-point equality");
   UC04_Record("PRICE_TOLERANCE_FAIL", !AL_UC04PricesCloseEnough(_Symbol, 1.0, 1.0 + point), "full-point inequality");
}

void UC04_TestObjects(void)
{
   string keep = UC04_TEST_PREFIX + "KEEP";
   string del1 = UC04_TEST_PREFIX + "DEL_1";
   string del2 = UC04_TEST_PREFIX + "DEL_2";
   ObjectDelete(0, keep);
   ObjectDelete(0, del1);
   ObjectDelete(0, del2);

   datetime t = TimeCurrent();
   double price = SymbolInfoDouble(_Symbol, SYMBOL_BID);
   if(price <= 0.0)
      price = 1.0;

   ObjectCreate(0, keep, OBJ_VLINE, 0, t, 0.0);
   ObjectCreate(0, del1, OBJ_VLINE, 0, t, 0.0);
   ObjectCreate(0, del2, OBJ_VLINE, 0, t, 0.0);
   int deleted = AL_UC04DeleteObjectsByPrefix(0, UC04_TEST_PREFIX + "DEL_");
   bool delete_ok = deleted == 2 && ObjectFind(0, keep) >= 0 && ObjectFind(0, del1) < 0 && ObjectFind(0, del2) < 0;
   UC04_Record("OBJECT_DELETE_PREFIX", delete_ok, "owned prefix only");

   string arrow = UC04_TEST_PREFIX + "ARROW";
   int created = 0;
   bool arrow_ok = AL_UC04CreateArrow(0, arrow, t, price, clrWhite, 159, 2, created);
   arrow_ok = arrow_ok && created == 1 && ObjectFind(0, arrow) >= 0;
   UC04_Record("OBJECT_CREATE_ARROW", arrow_ok, "arrow creation and count side effect");

   ObjectDelete(0, keep);
   ObjectDelete(0, arrow);
}

void UC04_TestMarketStream(void)
{
   DALBar bars[];
   int count = 0;
   datetime last_closed = 0;
   datetime analysis_start = 0;
   bool appended = AL_UC04UpdateLiveBarStream(
      _Symbol,
      (ENUM_TIMEFRAMES)_Period,
      32,
      bars,
      count,
      last_closed,
      analysis_start
   );
   bool state_ok = (!appended || (count > 0 && last_closed > 0 && analysis_start > 0));
   UC04_Record("MARKET_STREAM_STATE", state_ok, "append result and owned state remain coherent");
}

void OnStart(void)
{
   g_uc04_handle = FileOpen(
      UC04_TEST_OUTPUT,
      FILE_WRITE | FILE_CSV | FILE_ANSI | FILE_COMMON,
      ','
   );
   if(g_uc04_handle != INVALID_HANDLE)
      FileWrite(g_uc04_handle, "test_id", "status", "detail");

   UC04_TestTimeframe();
   UC04_TestDateTime();
   UC04_TestClosedBarClock();
   UC04_TestConfigurationGates();
   UC04_TestM0001Config();
   UC04_TestM0002Config();
   UC04_TestDayeTimeConfig();
   UC04_TestFileLifecycle();
   UC04_TestPriceTolerance();
   UC04_TestObjects();
   UC04_TestMarketStream();

   string overall = (g_uc04_failed == 0 ? "PASS" : "FAIL");
   if(g_uc04_handle != INVALID_HANDLE)
   {
      FileWrite(g_uc04_handle, "SUMMARY", overall, StringFormat("passed=%d;failed=%d", g_uc04_passed, g_uc04_failed));
      FileClose(g_uc04_handle);
      g_uc04_handle = INVALID_HANDLE;
   }

   Print("UC04_SELFTEST_SUMMARY|", overall, "|passed=", g_uc04_passed, "|failed=", g_uc04_failed);
}
