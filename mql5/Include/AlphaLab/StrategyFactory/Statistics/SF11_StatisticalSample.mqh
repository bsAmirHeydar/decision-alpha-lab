#ifndef __SF11_STATISTICAL_SAMPLE_MQH__
#define __SF11_STATISTICAL_SAMPLE_MQH__
#include "SF11_StatisticsEnums.mqh"
#include "../Research/SF10_AllResearch.mqh"
struct SF11_StatisticalSample
{
   string schema;
   string sample_id;
   string outcome_id;
   string candidate_id;
   string event_id;
   string cluster_id;
   string strategy_id;
   string symbol;
   string direction;
   string session_id;
   int year;
   int month;
   int weekday;
   string stratum_key;
   bool filled;
   bool ambiguous;
   double net_r;
   double mfe_r;
   double mae_r;
   double holding_seconds;
   double weight;
   long known_time_utc_msc;
};
bool SF11_ValidateStatisticalSample(const SF11_StatisticalSample &s,string &error)
{
   if(s.schema!="alpha_lab.strategy_factory/statistical_sample@1.0.0")
   {error="unsupported statistical sample schema";return false;}
   if(!SF01_IsSafeIdentifier(s.sample_id,128)||!SF01_IsSafeIdentifier(s.outcome_id,128)||
      !SF01_IsSafeIdentifier(s.candidate_id,128)||!SF01_IsSafeIdentifier(s.event_id,128)||
      !SF01_IsSafeIdentifier(s.cluster_id,128)||!SF01_IsSafeIdentifier(s.strategy_id,128)||
      !SF01_IsTerminalSymbol(s.symbol)||!SF01_IsSafeIdentifier(s.stratum_key,256))
   {error="invalid statistical sample identity";return false;}
   if(!MathIsValidNumber(s.net_r)||!MathIsValidNumber(s.mfe_r)||!MathIsValidNumber(s.mae_r)||
      !MathIsValidNumber(s.holding_seconds)||!MathIsValidNumber(s.weight)||s.mfe_r<0.0||
      s.mae_r<0.0||s.holding_seconds<0.0||s.weight<=0.0||s.month<1||s.month>12||
      s.weekday<0||s.weekday>6||s.known_time_utc_msc<0)
   {error="invalid statistical sample values";return false;}
   error="";return true;
}
#endif
