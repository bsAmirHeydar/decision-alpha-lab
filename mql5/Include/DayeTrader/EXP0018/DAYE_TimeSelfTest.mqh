#ifndef __EXP0018_DAYE_TIME_SELF_TEST_MQH__
#define __EXP0018_DAYE_TIME_SELF_TEST_MQH__

#include <DayeTrader/EXP0018/DAYE_Diagnostics.mqh>

bool DAYE_AssertEqualInt(const string name,const int actual,const int expected,int &failures)
{
   if(actual == expected)
      return true;
   failures++;
   Print("EXP0018 P01 self-test FAIL ",name," actual=",actual," expected=",expected);
   return false;
}

bool DAYE_AssertEqualString(const string name,const string actual,const string expected,int &failures)
{
   if(actual == expected)
      return true;
   failures++;
   Print("EXP0018 P01 self-test FAIL ",name," actual=",actual," expected=",expected);
   return false;
}

bool DAYE_AssertEqualTime(const string name,const datetime actual,const datetime expected,int &failures)
{
   if(actual == expected)
      return true;
   failures++;
   Print("EXP0018 P01 self-test FAIL ",name," actual=",DAYE_FormatDateTime(actual)," expected=",DAYE_FormatDateTime(expected));
   return false;
}

bool DAYE_RunEmbeddedTimeSelfTests(void)
{
   int failures = 0;

   DAYE_TimeConfig config;
   config.schema_version = DAYE_TIME_SCHEMA_VERSION;
   config.broker_offset_mode = DAYE_BROKER_OFFSET_MANUAL_FIXED;
   config.broker_utc_offset_minutes = 0;
   config.ny_offset_mode = DAYE_NY_AUTO_US_DST;
   config.manual_new_york_utc_offset_minutes = -300;
   config.ambiguous_start_policy = DAYE_LOCAL_EARLIEST;
   config.ambiguous_end_policy = DAYE_LOCAL_LATEST;

   MqlDateTime parts;
   ZeroMemory(parts);
   parts.year=2026; parts.mon=3; parts.day=8; parts.hour=6; parts.min=59; parts.sec=0;
   datetime pre_spring = StructToTime(parts);
   datetime ny = 0;
   bool dst = false;
   int offset = 0;
   int fold = 0;
   string reason = "";
   DAYE_UtcToNewYork(pre_spring,config,ny,dst,offset,fold,reason);
   DAYE_AssertEqualInt("spring_pre_offset",offset,-300,failures);
   DAYE_AssertEqualString("spring_pre_ny",TimeToString(ny,TIME_DATE|TIME_MINUTES),"2026.03.08 01:59",failures);

   parts.hour=7; parts.min=0;
   datetime post_spring = StructToTime(parts);
   DAYE_UtcToNewYork(post_spring,config,ny,dst,offset,fold,reason);
   DAYE_AssertEqualInt("spring_post_offset",offset,-240,failures);
   DAYE_AssertEqualString("spring_post_ny",TimeToString(ny,TIME_DATE|TIME_MINUTES),"2026.03.08 03:00",failures);

   ZeroMemory(parts);
   parts.year=2026; parts.mon=11; parts.day=1; parts.hour=5; parts.min=59;
   datetime pre_fall = StructToTime(parts);
   DAYE_UtcToNewYork(pre_fall,config,ny,dst,offset,fold,reason);
   DAYE_AssertEqualInt("fall_pre_offset",offset,-240,failures);
   DAYE_AssertEqualInt("fall_pre_fold",fold,0,failures);

   parts.hour=6; parts.min=0;
   datetime post_fall = StructToTime(parts);
   DAYE_UtcToNewYork(post_fall,config,ny,dst,offset,fold,reason);
   DAYE_AssertEqualInt("fall_post_offset",offset,-300,failures);
   DAYE_AssertEqualInt("fall_post_fold",fold,1,failures);
   DAYE_AssertEqualString("fall_post_ny",TimeToString(ny,TIME_DATE|TIME_MINUTES),"2026.11.01 01:00",failures);

   DAYE_AssertEqualInt("session_175959",(int)DAYE_ClassifySessionBySecond(17*3600+59*60+59),(int)DAYE_PERIOD_NONE,failures);
   DAYE_AssertEqualInt("session_180000",(int)DAYE_ClassifySessionBySecond(18*3600),(int)DAYE_PERIOD_A,failures);
   DAYE_AssertEqualInt("subcycle_162959",(int)DAYE_ClassifySubcycleBySecond(16*3600+29*60+59),(int)DAYE_PERIOD_P3,failures);
   DAYE_AssertEqualInt("subcycle_163000",(int)DAYE_ClassifySubcycleBySecond(16*3600+30*60),(int)DAYE_PERIOD_P4,failures);
   DAYE_AssertEqualInt("subcycle_170000",(int)DAYE_ClassifySubcycleBySecond(17*3600),(int)DAYE_PERIOD_NONE,failures);

   MqlDateTime key_parts;
   ZeroMemory(key_parts);
   key_parts.year=2026; key_parts.mon=7; key_parts.day=10; key_parts.hour=17; key_parts.min=59; key_parts.sec=59;
   DAYE_AssertEqualString("day_key_before_18",DAYE_TradingDayKeyNy(StructToTime(key_parts)),"2026-07-09",failures);
   key_parts.hour=18; key_parts.min=0; key_parts.sec=0;
   DAYE_AssertEqualString("day_key_at_18",DAYE_TradingDayKeyNy(StructToTime(key_parts)),"2026-07-10",failures);

   if(failures == 0)
   {
      Print("EXP0018 P01 embedded self-tests PASS");
      return true;
   }
   Print("EXP0018 P01 embedded self-tests FAIL count=",failures);
   return false;
}

#endif
