#ifndef __CGX_UTILITIES_MQH__
#define __CGX_UTILITIES_MQH__

#include <IntermarketDivergenceExecution/CG/Execution/CGX_Types.mqh>

string CGX_RuntimeText(const ECGXRuntimeMode mode)
{
   if(mode==CGX_RUNTIME_BACKTEST_ONLY) return "BACKTEST_ONLY";
   if(mode==CGX_RUNTIME_PAPER_ONLY) return "PAPER_ONLY";
   if(mode==CGX_RUNTIME_LIVE_ENABLED) return "LIVE_ENABLED";
   return "UNKNOWN";
}

string CGX_TradeLegText(const ECGXTradeLeg leg)
{
   if(leg==CGX_TRADE_PROTECTED_SYMBOL) return "PROTECTED";
   if(leg==CGX_TRADE_HUNTER_SYMBOL) return "HUNTER";
   return "UNKNOWN";
}

string CGX_TargetModelText(const ECGXTargetModel model)
{
   if(model==CGX_TARGET_ATR_MULTIPLE) return "ATR_MULTIPLE";
   if(model==CGX_TARGET_RISK_MULTIPLE) return "RISK_MULTIPLE";
   return "UNKNOWN";
}

string CGX_VolumeModelText(const ECGXVolumeModel model)
{
   if(model==CGX_VOLUME_FIXED_RISK_MONEY) return "FIXED_RISK_MONEY";
   if(model==CGX_VOLUME_RISK_PERCENT_EQUITY) return "RISK_PERCENT_EQUITY";
   if(model==CGX_VOLUME_FIXED_LOTS) return "FIXED_LOTS";
   return "UNKNOWN";
}

string CGX_DirectionText(const ECGCSignalDirection direction)
{
   if(direction==CGC_DIRECTION_BUY) return "BUY";
   if(direction==CGC_DIRECTION_SELL) return "SELL";
   return "NONE";
}

int CGX_PriceDigits(const string symbol)
{
   if(symbol=="")
      return 5;
   int digits=(int)SymbolInfoInteger(symbol,SYMBOL_DIGITS);
   if(digits<0) digits=0;
   return digits;
}

double CGX_NormalizePrice(const string symbol,const double price)
{
   return NormalizeDouble(price,CGX_PriceDigits(symbol));
}

int CGX_VolumeDigits(const double step)
{
   if(step<=0.0)
      return 2;
   for(int digits=0;digits<=8;digits++)
   {
      if(MathAbs(NormalizeDouble(step,digits)-step)<=1e-12)
         return digits;
   }
   return 8;
}

double CGX_NormalizeVolumeDown(const double volume,const double step)
{
   if(volume<=0.0 || step<=0.0)
      return 0.0;
   double units=MathFloor((volume/step)+1e-10);
   return NormalizeDouble(units*step,CGX_VolumeDigits(step));
}

uint CGX_Fnv1a32(const string text)
{
   uint hash=2166136261;
   int length=StringLen(text);
   for(int i=0;i<length;i++)
   {
      uint code=(uint)StringGetCharacter(text,i);
      hash^=code;
      hash*=16777619;
   }
   return hash;
}

string CGX_ShortSignalHash(const string signal_id)
{
   uint hash=CGX_Fnv1a32(signal_id);
   return IntegerToString((int)(hash & 0x7FFFFFFF));
}

string CGX_BuildOrderComment(const SCGXTradePlan &plan)
{
   string leg=(plan.trade_leg==CGX_TRADE_PROTECTED_SYMBOL ? "P" : "H");
   string result=StringFormat("E17|%dm|%s|%s",plan.group_minutes,leg,CGX_ShortSignalHash(plan.signal_id));
   if(StringLen(result)>31)
      result=StringSubstr(result,0,31);
   return result;
}

bool CGX_IsTesterRuntime()
{
   return ((bool)MQLInfoInteger(MQL_TESTER) || (bool)MQLInfoInteger(MQL_OPTIMIZATION));
}

bool CGX_IsHedgingAccount()
{
   ENUM_ACCOUNT_MARGIN_MODE mode=(ENUM_ACCOUNT_MARGIN_MODE)AccountInfoInteger(ACCOUNT_MARGIN_MODE);
   return (mode==ACCOUNT_MARGIN_MODE_RETAIL_HEDGING);
}

bool CGX_IsMagicOwned(const long magic,const long magic_base)
{
   return (magic>=magic_base && magic<magic_base+CGT_GROUP_COUNT);
}

#endif
