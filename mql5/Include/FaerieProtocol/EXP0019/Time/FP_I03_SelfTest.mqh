#ifndef __EXP0019_FP_I03_SELF_TEST_MQH__
#define __EXP0019_FP_I03_SELF_TEST_MQH__

#include "FP_I03_Diagnostics.mqh"

void FP_I03_Check(const bool condition,const string name,FP_I03_SelfTestResult &r)
  {
   r.check_count++;if(condition)r.pass_count++;else{r.fail_count++;r.latest_failed_check=name;}
  }

bool FP_I03_RunSelfTest(FP_I03_SelfTestResult &r)
  {
   ZeroMemory(r);FP_I03_TimeKernelConfig config;FP_I03_DefaultConfig(config);string reason="";
   FP_I03_Check(FP_I03_ValidateConfig(config,reason),"config",r);
   FP_I03_Check(DAYE_NewYorkDstStartUtc(2026)==StringToTime("2026.03.08 07:00:00"),"dst_start",r);
   FP_I03_Check(DAYE_NewYorkDstEndUtc(2026)==StringToTime("2026.11.01 06:00:00"),"dst_end",r);
   FP_I03_Check(FP_I03_ClassifyIntraday(18*3600)==FP_I03_SEGMENT_A,"a_start",r);
   FP_I03_Check(FP_I03_ClassifyIntraday(4*3600)==FP_I03_SEGMENT_L,"l_start",r);
   FP_I03_Check(FP_I03_ClassifyIntraday(9*3600+30*60)==FP_I03_SEGMENT_N,"n_start",r);
   FP_I03_Check(FP_I03_ClassifyIntraday(17*3600)==FP_I03_SEGMENT_DAILY_GAP,"gap_start",r);
   FP_I03_TradingDayWindow td;FP_I03_Check(FP_I03_BuildTradingDay("2026-07-13",config,td,reason),"trading_day",r);
   FP_I03_Check(td.elapsed_seconds==23*3600,"trading_day_duration",r);
   FP_I03_SessionWindow a,l,n;
   FP_I03_Check(FP_I03_BuildSession("2026-07-13",FP_I03_SEGMENT_A,0,config,a,reason),"session_a",r);
   FP_I03_Check(FP_I03_BuildSession("2026-07-13",FP_I03_SEGMENT_L,0,config,l,reason),"session_l",r);
   FP_I03_Check(FP_I03_BuildSession("2026-07-13",FP_I03_SEGMENT_N,0,config,n,reason),"session_n",r);
   FP_I03_Check(a.elapsed_seconds==10*3600,"a_duration",r);
   FP_I03_Check(l.elapsed_seconds==5*3600+30*60,"l_duration",r);
   FP_I03_Check(n.elapsed_seconds==7*3600+30*60,"n_duration",r);
   datetime sunday=StringToTime("2026.07.12 00:00:00");FP_I03_WeekWindow week;
   FP_I03_Check(FP_I03_BuildWeek(sunday,0,config,week,reason),"week",r);
   FP_I03_Check(week.elapsed_seconds==119*3600,"week_duration",r);
   FP_I03_LocalResolution ambiguous;FP_I03_ResolveLocal(StringToTime("2026.11.01 01:30:00"),FP_I03_LOCAL_REJECT,config,ambiguous);
   FP_I03_Check(ambiguous.candidate_count==2,"fall_ambiguous",r);
   FP_I03_LocalResolution missing;FP_I03_ResolveLocal(StringToTime("2026.03.08 02:30:00"),FP_I03_LOCAL_REJECT,config,missing);
   FP_I03_Check(missing.candidate_count==0,"spring_nonexistent",r);
   r.evidence_key=FP_I02_CompactId("FPI03TEST",IntegerToString(r.check_count)+"|"+IntegerToString(r.pass_count)+"|"+r.latest_failed_check);
   return (r.fail_count==0);
  }

#endif
