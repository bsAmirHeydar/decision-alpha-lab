#ifndef __SF18_REQUEST_BUILDER_MQH__
#define __SF18_REQUEST_BUILDER_MQH__
#include "SF18_LiveLedger.mqh"

bool SF18_SelectFillingPolicy(const string symbol,const bool pending,ENUM_ORDER_TYPE_FILLING &filling,string &error)
{
   if(pending)
   {
      filling=ORDER_FILLING_RETURN;
      error="";
      return true;
   }
   const ENUM_SYMBOL_TRADE_EXECUTION execution=(ENUM_SYMBOL_TRADE_EXECUTION)SymbolInfoInteger(symbol,SYMBOL_TRADE_EXEMODE);
   const int allowed=(int)SymbolInfoInteger(symbol,SYMBOL_FILLING_MODE);
   if(execution!=SYMBOL_TRADE_EXECUTION_MARKET)
   {
      filling=ORDER_FILLING_RETURN;
      error="";
      return true;
   }
   if((allowed&SYMBOL_FILLING_FOK)==SYMBOL_FILLING_FOK)
   {
      filling=ORDER_FILLING_FOK;
      error="";
      return true;
   }
   if((allowed&SYMBOL_FILLING_IOC)==SYMBOL_FILLING_IOC)
   {
      filling=ORDER_FILLING_IOC;
      error="";
      return true;
   }
   error="no supported market filling policy";
   return false;
}

bool SF18_OrderKindAllowed(const string symbol,const ENUM_SF08_ORDER_KIND kind)
{
   const int allowed=(int)SymbolInfoInteger(symbol,SYMBOL_ORDER_MODE);
   if(kind==SF08_ORDER_MARKET)return (allowed&SYMBOL_ORDER_MARKET)==SYMBOL_ORDER_MARKET;
   if(kind==SF08_ORDER_LIMIT)return (allowed&SYMBOL_ORDER_LIMIT)==SYMBOL_ORDER_LIMIT;
   if(kind==SF08_ORDER_STOP)return (allowed&SYMBOL_ORDER_STOP)==SYMBOL_ORDER_STOP;
   return false;
}

bool SF18_BuildOpenRequest(const SF16_ExecutionIntent &intent,const SF18_QuoteSnapshot &quote,const SF18_SafetyPolicy &policy,const ulong magic,MqlTradeRequest &request,string &request_id,string &error)
{
   ZeroMemory(request);
   if(!SF18_OrderKindAllowed(intent.symbol,intent.order_kind))
   {
      error="order kind not allowed by symbol";
      return false;
   }
   const bool pending=(intent.order_kind!=SF08_ORDER_MARKET);
   request.action=pending?TRADE_ACTION_PENDING:TRADE_ACTION_DEAL;
   request.magic=magic;
   request.symbol=intent.symbol;
   request.volume=intent.volume;
   request.deviation=(ulong)policy.maximum_deviation_points;
   request.sl=intent.stop_price;
   request.tp=intent.has_target?intent.target_price:0.0;
   request.comment="SF18:"+StringSubstr(intent.intent_id,0,20);
   if(intent.order_kind==SF08_ORDER_MARKET)
   {
      request.type=intent.direction==1?ORDER_TYPE_BUY:ORDER_TYPE_SELL;
      request.price=intent.direction==1?quote.ask:quote.bid;
   }
   else if(intent.order_kind==SF08_ORDER_LIMIT)
   {
      request.type=intent.direction==1?ORDER_TYPE_BUY_LIMIT:ORDER_TYPE_SELL_LIMIT;
      request.price=intent.entry_price;
   }
   else if(intent.order_kind==SF08_ORDER_STOP)
   {
      request.type=intent.direction==1?ORDER_TYPE_BUY_STOP:ORDER_TYPE_SELL_STOP;
      request.price=intent.entry_price;
   }
   else
   {
      error="unsupported order kind";
      return false;
   }
   if(!SF18_SelectFillingPolicy(intent.symbol,pending,request.type_filling,error))return false;
   if(pending)
   {
      const int expiration_flags=(int)SymbolInfoInteger(intent.symbol,SYMBOL_EXPIRATION_MODE);
      if((expiration_flags&SYMBOL_EXPIRATION_SPECIFIED)==SYMBOL_EXPIRATION_SPECIFIED)
      {
         request.type_time=ORDER_TIME_SPECIFIED;
         request.expiration=(datetime)(intent.expires_at_utc_msc/1000);
      }
      else request.type_time=ORDER_TIME_GTC;
   }
   else request.type_time=ORDER_TIME_GTC;
   const string canonical=intent.intent_id+"|"+intent.intent_hash+"|"+IntegerToString((int)request.action)+"|"+intent.symbol+"|"+IntegerToString((int)request.type)+"|"+IntegerToString((int)request.type_filling)+"|"+IntegerToString((int)request.type_time)+"|"+SF01_CanonicalDouble(request.volume)+"|"+SF01_CanonicalDouble(request.price)+"|"+SF01_CanonicalDouble(request.sl)+"|"+SF01_CanonicalDouble(request.tp)+"|"+IntegerToString((long)magic)+"|"+IntegerToString(intent.expires_at_utc_msc);
   request_id=SF01_StableId("lreq",canonical);
   error="";
   return true;
}
#endif
