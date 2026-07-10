#ifndef __EXP0018_DAYE_SYMBOL_RESOLVER_MQH__
#define __EXP0018_DAYE_SYMBOL_RESOLVER_MQH__

#include <DayeTrader/EXP0018/DAYE_SymbolContract.mqh>

// Broker-neutral symbol resolution for the chart-facing EXP0018 visual Expert.
// Resolution affects only broker symbol names. Canonical identities remain SPX/NDX
// (or the explicit canonical inputs) and no market doctrine is inferred here.

string DAYE_SR_Normalize(string value)
{
   StringTrimLeft(value);
   StringTrimRight(value);
   StringToUpper(value);
   StringReplace(value,"#","");
   StringReplace(value,".","");
   StringReplace(value,"_","");
   StringReplace(value,"-","");
   StringReplace(value," ","");
   StringReplace(value,"/","");
   StringReplace(value,"\\","");
   StringReplace(value,"&","AND");
   return value;
}

bool DAYE_SR_SymbolExists(const string symbol)
{
   if(symbol=="") return false;
   bool is_custom=false;
   return SymbolExist(symbol,is_custom);
}

int DAYE_SR_CanonicalKind(const string canonical_symbol)
{
   string value=DAYE_SR_Normalize(canonical_symbol);
   if(StringFind(value,"NDX")>=0 || StringFind(value,"NASDAQ")>=0 ||
      StringFind(value,"NDAQ")>=0 || value=="US100" || value=="NAS100" ||
      value=="USTEC" || value=="NQ100") return 2;
   if(StringFind(value,"SPX")>=0 || StringFind(value,"SANDP")>=0 ||
      value=="US500" || value=="SP500" || value=="SPX500" || value=="USA500") return 1;
   return 0;
}

int DAYE_SR_MaxInt(const int a,const int b)
{
   return (a>b?a:b);
}

int DAYE_SR_AliasScore(const string symbol,const string canonical_symbol)
{
   string value=DAYE_SR_Normalize(symbol);
   string canonical=DAYE_SR_Normalize(canonical_symbol);
   int kind=DAYE_SR_CanonicalKind(canonical_symbol);
   int score=0;

   if(value==canonical && canonical!="") score=120;

   if(kind==2)
   {
      if(value=="NDXUSD" || value=="NDX" || value=="US100" || value=="USTEC" ||
         value=="NAS100" || value=="NASDAQ100" || value=="USNDAQ100" ||
         value=="NQ100" || value=="USA100") score=DAYE_SR_MaxInt(score,115);
      if(StringFind(value,"USNDAQ100")>=0) score=DAYE_SR_MaxInt(score,112);
      if(StringFind(value,"NASDAQ100")>=0) score=DAYE_SR_MaxInt(score,110);
      if(StringFind(value,"NAS100")>=0) score=DAYE_SR_MaxInt(score,105);
      if(StringFind(value,"US100")>=0) score=DAYE_SR_MaxInt(score,103);
      if(StringFind(value,"USTEC")>=0) score=DAYE_SR_MaxInt(score,101);
      if(StringFind(value,"NDX")>=0) score=DAYE_SR_MaxInt(score,98);
      if(StringFind(value,"NQ100")>=0) score=DAYE_SR_MaxInt(score,94);
      if(StringFind(value,"US500")>=0 || StringFind(value,"SPX")>=0 || StringFind(value,"SP500")>=0)
         score-=80;
   }
   else if(kind==1)
   {
      if(value=="SPXUSD" || value=="SPX" || value=="US500" || value=="SP500" ||
         value=="SPX500" || value=="USSPX500" || value=="USA500" || value=="SANDP500")
         score=DAYE_SR_MaxInt(score,115);
      if(StringFind(value,"USSPX500")>=0) score=DAYE_SR_MaxInt(score,112);
      if(StringFind(value,"SPX500")>=0) score=DAYE_SR_MaxInt(score,108);
      if(StringFind(value,"US500")>=0) score=DAYE_SR_MaxInt(score,106);
      if(StringFind(value,"SP500")>=0) score=DAYE_SR_MaxInt(score,104);
      if(StringFind(value,"SPX")>=0) score=DAYE_SR_MaxInt(score,100);
      if(StringFind(value,"SANDP500")>=0) score=DAYE_SR_MaxInt(score,98);
      if(StringFind(value,"US100")>=0 || StringFind(value,"NASDAQ")>=0 || StringFind(value,"NDX")>=0)
         score-=80;
   }
   else if(canonical!="" && StringFind(value,canonical)>=0)
      score=DAYE_SR_MaxInt(score,80);

   string description=SymbolInfoString(symbol,SYMBOL_DESCRIPTION);
   description=DAYE_SR_Normalize(description);
   if(kind==2 && (StringFind(description,"NASDAQ100")>=0 || StringFind(description,"NASDAQ")>=0)) score+=8;
   if(kind==1 && (StringFind(description,"SANDP500")>=0 || StringFind(description,"SP500")>=0)) score+=8;

   long visible=0;
   long selected=0;
   if(SymbolInfoInteger(symbol,SYMBOL_VISIBLE,visible) && visible!=0) score+=6;
   if(SymbolInfoInteger(symbol,SYMBOL_SELECT,selected) && selected!=0) score+=3;
   return score;
}

bool DAYE_SR_SelectResolved(const string symbol,string &reason)
{
   reason="";
   if(!DAYE_SR_SymbolExists(symbol))
   {
      reason="resolved_symbol_does_not_exist";
      return false;
   }
   ResetLastError();
   if(!SymbolSelect(symbol,true))
   {
      reason="resolved_symbol_select_failed_"+IntegerToString(GetLastError());
      return false;
   }
   return true;
}

bool DAYE_ResolveBrokerSymbol(const string requested_symbol,
                              const string canonical_symbol,
                              const string current_chart_symbol,
                              const bool auto_resolve,
                              const bool prefer_current_chart,
                              string &resolved_symbol,
                              string &reason)
{
   resolved_symbol="";
   reason="";

   if(prefer_current_chart && DAYE_SR_SymbolExists(current_chart_symbol))
   {
      int current_score=DAYE_SR_AliasScore(current_chart_symbol,canonical_symbol);
      if(current_score>=90)
      {
         string select_reason="";
         if(DAYE_SR_SelectResolved(current_chart_symbol,select_reason))
         {
            resolved_symbol=current_chart_symbol;
            reason="current_chart_alias_score_"+IntegerToString(current_score);
            return true;
         }
      }
   }

   if(DAYE_SR_SymbolExists(requested_symbol))
   {
      string select_reason="";
      if(DAYE_SR_SelectResolved(requested_symbol,select_reason))
      {
         resolved_symbol=requested_symbol;
         reason="configured_symbol_exact";
         return true;
      }
      reason=select_reason;
      if(!auto_resolve) return false;
   }
   else if(!auto_resolve)
   {
      reason="configured_symbol_not_found_and_auto_resolution_disabled";
      return false;
   }

   int best_score=-1000000;
   string best_symbol="";
   int total=SymbolsTotal(false);
   for(int i=0;i<total;i++)
   {
      string candidate=SymbolName(i,false);
      if(candidate=="") continue;
      int score=DAYE_SR_AliasScore(candidate,canonical_symbol);
      if(score>best_score)
      {
         best_score=score;
         best_symbol=candidate;
      }
   }

   if(best_symbol=="" || best_score<90)
   {
      reason="no_high_confidence_broker_alias_for_"+canonical_symbol+"_best_score_"+IntegerToString(best_score);
      return false;
   }

   string select_reason="";
   if(!DAYE_SR_SelectResolved(best_symbol,select_reason))
   {
      reason=select_reason;
      return false;
   }
   resolved_symbol=best_symbol;
   reason="market_watch_alias_score_"+IntegerToString(best_score);
   return true;
}

bool DAYE_ResolveBrokerPair(const string requested_a,const string canonical_a,
                            const string requested_b,const string canonical_b,
                            const string current_chart_symbol,
                            const bool auto_resolve,const bool prefer_current_chart,
                            string &resolved_a,string &resolved_b,string &report)
{
   string reason_a="";
   string reason_b="";
   bool ok_a=DAYE_ResolveBrokerSymbol(requested_a,canonical_a,current_chart_symbol,
                                      auto_resolve,prefer_current_chart,resolved_a,reason_a);
   bool ok_b=DAYE_ResolveBrokerSymbol(requested_b,canonical_b,current_chart_symbol,
                                      auto_resolve,prefer_current_chart,resolved_b,reason_b);
   if(ok_a && ok_b && resolved_a==resolved_b)
   {
      ok_a=false;
      ok_b=false;
      reason_a="resolved_pair_collapsed_to_same_symbol";
      reason_b=reason_a;
   }
   report="A["+canonical_a+"] requested="+requested_a+" resolved="+resolved_a+" reason="+reason_a+
          " | B["+canonical_b+"] requested="+requested_b+" resolved="+resolved_b+" reason="+reason_b;
   return ok_a && ok_b;
}

#endif
