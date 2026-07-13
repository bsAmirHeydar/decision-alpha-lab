#ifndef __EXP0019_FP_I04_BAR_VALIDATION_MQH__
#define __EXP0019_FP_I04_BAR_VALIDATION_MQH__
#include "FP_I04_SymbolPair.mqh"
bool FP_I04_IsMinuteAligned(const datetime value){return ((long)value%FP_I04_M1_SECONDS)==0;}
bool FP_I04_IsOnTickGrid(const double value,const double tick_size){if(tick_size<=0.0)return false;double units=value/tick_size;return MathAbs(units-MathRound(units))<=1e-7;}
bool FP_I04_ValidateBar(const FP_I04_M1Bar &b,const FP_I04_SymbolSpec &s,string &reason)
  { if(b.canonical_symbol!=s.canonical_symbol){reason="FP_DRC_BAR_SYMBOL_MISMATCH";return false;}if(!FP_I04_IsMinuteAligned(b.open_utc)){reason="FP_DRC_M1_ALIGNMENT_INVALID";return false;}if(b.finality!=FP_I04_BAR_CLOSED){reason="FP_DRC_PROVISIONAL_BAR_FORBIDDEN";return false;}if(b.high<b.low || b.high<MathMax(b.open,b.close) || b.low>MathMin(b.open,b.close)){reason="FP_DRC_OHLC_INVALID";return false;}if(!FP_I04_IsOnTickGrid(b.open,s.tick_size)||!FP_I04_IsOnTickGrid(b.high,s.tick_size)||!FP_I04_IsOnTickGrid(b.low,s.tick_size)||!FP_I04_IsOnTickGrid(b.close,s.tick_size)){reason="FP_DRC_PRICE_OFF_TICK_GRID";return false;}if(b.tick_volume<0||b.real_volume<0||b.spread_points<0){reason="FP_DRC_VOLUME_SPREAD_INVALID";return false;}reason="FP_DRC_BAR_UNIQUE";return true; }
string FP_I04_BarHash(const FP_I04_M1Bar &b){return FP_I02_CompactId("FPM1",b.canonical_symbol+"|"+IntegerToString((long)b.open_utc)+"|"+DoubleToString(b.open,8)+"|"+DoubleToString(b.high,8)+"|"+DoubleToString(b.low,8)+"|"+DoubleToString(b.close,8)+"|"+b.source_revision);}
#endif
