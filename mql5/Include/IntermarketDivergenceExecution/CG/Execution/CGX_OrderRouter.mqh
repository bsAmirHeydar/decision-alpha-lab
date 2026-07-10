#ifndef __CGX_ORDER_ROUTER_MQH__
#define __CGX_ORDER_ROUTER_MQH__

#include <Trade/Trade.mqh>
#include <IntermarketDivergenceExecution/CG/Execution/CGX_Utilities.mqh>

class CCGX_OrderRouter
{
private:
   SCGXExecutionConfig m_config;
   CTrade              m_trade;

   void ResetResult(SCGXExecutionResult &result)
   {
      result.attempted=false;
      result.sent=false;
      result.paper_only=false;
      result.order_ticket=0;
      result.deal_ticket=0;
      result.retcode=0;
      result.result_price=0.0;
      result.message="";
   }

   bool SuccessfulRetcode(const uint retcode)
   {
      return (retcode==TRADE_RETCODE_DONE ||
              retcode==TRADE_RETCODE_DONE_PARTIAL ||
              retcode==TRADE_RETCODE_PLACED);
   }

   bool DirectionAllowedBySymbol(const string symbol,const ECGCSignalDirection direction,string &reason)
   {
      ENUM_SYMBOL_TRADE_MODE mode=(ENUM_SYMBOL_TRADE_MODE)SymbolInfoInteger(symbol,SYMBOL_TRADE_MODE);
      if(mode==SYMBOL_TRADE_MODE_DISABLED || mode==SYMBOL_TRADE_MODE_CLOSEONLY)
      {
         reason="symbol_trade_mode_blocks_entry";
         return false;
      }
      if(direction==CGC_DIRECTION_BUY && mode==SYMBOL_TRADE_MODE_SHORTONLY)
      {
         reason="symbol_is_short_only";
         return false;
      }
      if(direction==CGC_DIRECTION_SELL && mode==SYMBOL_TRADE_MODE_LONGONLY)
      {
         reason="symbol_is_long_only";
         return false;
      }
      reason="ok";
      return true;
   }

   bool HasAnyPositionOnSymbol(const string symbol)
   {
      for(int i=PositionsTotal()-1;i>=0;i--)
      {
         ulong ticket=PositionGetTicket(i);
         if(ticket==0)
            continue;
         if(PositionGetString(POSITION_SYMBOL)==symbol)
            return true;
      }
      return false;
   }

   bool HasOwnPositionOnSymbol(const string symbol)
   {
      for(int i=PositionsTotal()-1;i>=0;i--)
      {
         ulong ticket=PositionGetTicket(i);
         if(ticket==0)
            continue;
         if(PositionGetString(POSITION_SYMBOL)!=symbol)
            continue;
         long magic=PositionGetInteger(POSITION_MAGIC);
         if(CGX_IsMagicOwned(magic,m_config.magic_base))
            return true;
      }
      return false;
   }

   bool HasOwnOppositePosition(const string symbol,const ECGCSignalDirection direction)
   {
      for(int i=PositionsTotal()-1;i>=0;i--)
      {
         ulong ticket=PositionGetTicket(i);
         if(ticket==0)
            continue;
         if(PositionGetString(POSITION_SYMBOL)!=symbol)
            continue;
         long magic=PositionGetInteger(POSITION_MAGIC);
         if(!CGX_IsMagicOwned(magic,m_config.magic_base))
            continue;

         ENUM_POSITION_TYPE position_type=(ENUM_POSITION_TYPE)PositionGetInteger(POSITION_TYPE);
         if(direction==CGC_DIRECTION_BUY && position_type==POSITION_TYPE_SELL)
            return true;
         if(direction==CGC_DIRECTION_SELL && position_type==POSITION_TYPE_BUY)
            return true;
      }
      return false;
   }

   bool PositionPolicyAllows(const SCGXTradePlan &plan,string &reason)
   {
      if(!CGX_IsHedgingAccount())
      {
         if(m_config.netting_policy==CGX_NETTING_SKIP_WHEN_POSITION_EXISTS && HasAnyPositionOnSymbol(plan.trade_symbol))
         {
            reason="netting_account_position_already_exists";
            return false;
         }
      }
      if(!m_config.enable_hedging && HasOwnOppositePosition(plan.trade_symbol,plan.direction))
      {
         reason="hedging_disabled_opposite_position_exists";
         return false;
      }
      if(m_config.position_policy==CGX_POSITION_ONE_OWN_POSITION_SYMBOL && HasOwnPositionOnSymbol(plan.trade_symbol))
      {
         reason="own_position_already_exists_on_symbol";
         return false;
      }
      reason="ok";
      return true;
   }

   bool TransportAllowed(string &reason)
   {
      if(m_config.runtime_mode==CGX_RUNTIME_PAPER_ONLY)
      {
         reason="paper_only";
         return false;
      }
      if(m_config.runtime_mode==CGX_RUNTIME_BACKTEST_ONLY && !CGX_IsTesterRuntime())
      {
         reason="backtest_only_runtime_blocked_outside_tester";
         return false;
      }
      if(!(bool)MQLInfoInteger(MQL_TRADE_ALLOWED))
      {
         reason="mql_trade_not_allowed";
         return false;
      }
      if(!(bool)AccountInfoInteger(ACCOUNT_TRADE_ALLOWED))
      {
         reason="account_trade_not_allowed";
         return false;
      }
      reason="ok";
      return true;
   }

public:
   void Configure(const SCGXExecutionConfig &config)
   {
      m_config=config;
      m_trade.SetAsyncMode(false);
      m_trade.SetDeviationInPoints(m_config.deviation_points);
   }

   bool Execute(SCGXTradePlan &plan,SCGXExecutionResult &result)
   {
      ResetResult(result);
      if(!plan.valid)
      {
         result.message="invalid_trade_plan_"+plan.rejection_reason;
         return false;
      }

      string reason="";
      if(!DirectionAllowedBySymbol(plan.trade_symbol,plan.direction,reason))
      {
         result.message=reason;
         return false;
      }
      if(!PositionPolicyAllows(plan,reason))
      {
         result.message=reason;
         return false;
      }
      if(m_config.runtime_mode==CGX_RUNTIME_PAPER_ONLY)
      {
         result.paper_only=true;
         result.message="paper_plan_accepted_no_order_sent";
         return true;
      }
      if(!TransportAllowed(reason))
      {
         result.message=reason;
         return false;
      }

      m_trade.SetExpertMagicNumber(plan.magic_number);
      m_trade.SetDeviationInPoints(m_config.deviation_points);
      m_trade.SetTypeFillingBySymbol(plan.trade_symbol);
      ResetLastError();
      result.attempted=true;

      bool ok=false;
      if(plan.direction==CGC_DIRECTION_BUY)
         ok=m_trade.Buy(plan.volume,plan.trade_symbol,0.0,plan.stop_loss,plan.take_profit,plan.order_comment);
      else if(plan.direction==CGC_DIRECTION_SELL)
         ok=m_trade.Sell(plan.volume,plan.trade_symbol,0.0,plan.stop_loss,plan.take_profit,plan.order_comment);

      result.retcode=m_trade.ResultRetcode();
      result.order_ticket=m_trade.ResultOrder();
      result.deal_ticket=m_trade.ResultDeal();
      result.result_price=m_trade.ResultPrice();
      result.sent=(ok && SuccessfulRetcode(result.retcode));
      if(result.sent)
         result.message="order_sent_"+m_trade.ResultRetcodeDescription();
      else
         result.message="order_failed_"+m_trade.ResultRetcodeDescription()+"_error_"+IntegerToString(GetLastError());
      return result.sent;
   }
};

#endif
