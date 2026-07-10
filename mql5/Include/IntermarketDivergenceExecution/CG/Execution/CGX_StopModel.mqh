#ifndef __CGX_STOP_MODEL_MQH__
#define __CGX_STOP_MODEL_MQH__

#include <IntermarketDivergenceExecution/CG/Execution/CGX_EntryModel.mqh>

class CCGX_StopModel
{
public:
   bool Build(const SCGXExecutionConfig &config,const SCGXClosedCandle &candle,const ECGCSignalDirection direction,const double entry_price,double &stop_loss,string &reason)
   {
      if(config.stop_model!=CGX_STOP_BEHIND_CONFIRMATION_CANDLE)
      {
         reason="unsupported_stop_model";
         return false;
      }
      if(!candle.ready)
      {
         reason="confirmation_candle_not_ready";
         return false;
      }

      double point=SymbolInfoDouble(candle.symbol,SYMBOL_POINT);
      if(point<=0.0)
      {
         reason="invalid_symbol_point_for_stop";
         return false;
      }
      double buffer_points=config.stop_buffer_points;
      if(buffer_points<0.0)
         buffer_points=0.0;

      if(direction==CGC_DIRECTION_BUY)
         stop_loss=candle.low-(buffer_points*point);
      else if(direction==CGC_DIRECTION_SELL)
         stop_loss=candle.high+(buffer_points*point);
      else
      {
         reason="invalid_direction_for_stop";
         return false;
      }

      stop_loss=CGX_NormalizePrice(candle.symbol,stop_loss);
      if(direction==CGC_DIRECTION_BUY && !(stop_loss<entry_price))
      {
         reason="buy_stop_not_below_market_entry";
         return false;
      }
      if(direction==CGC_DIRECTION_SELL && !(stop_loss>entry_price))
      {
         reason="sell_stop_not_above_market_entry";
         return false;
      }

      reason="ok";
      return true;
   }
};

#endif
