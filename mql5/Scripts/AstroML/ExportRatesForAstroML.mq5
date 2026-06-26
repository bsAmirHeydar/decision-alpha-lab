#property strict
#property script_show_inputs

input string          InpSymbol      = "NAS100";
input ENUM_TIMEFRAMES InpTimeframe   = PERIOD_M1;
input datetime        InpFrom        = D'2022.01.01 00:00';
input datetime        InpTo          = D'2026.12.31 23:59';
input string          InpOutputName  = "astro_ml_prices_NAS100_M1.csv";
input bool            InpUseCommonFiles = true;

string TFToString(const ENUM_TIMEFRAMES tf)
{
   switch(tf)
   {
      case PERIOD_M1: return "M1";
      case PERIOD_M2: return "M2";
      case PERIOD_M3: return "M3";
      case PERIOD_M4: return "M4";
      case PERIOD_M5: return "M5";
      case PERIOD_M6: return "M6";
      case PERIOD_M10: return "M10";
      case PERIOD_M12: return "M12";
      case PERIOD_M15: return "M15";
      case PERIOD_M20: return "M20";
      case PERIOD_M30: return "M30";
      case PERIOD_H1: return "H1";
      case PERIOD_H2: return "H2";
      case PERIOD_H3: return "H3";
      case PERIOD_H4: return "H4";
      case PERIOD_H6: return "H6";
      case PERIOD_H8: return "H8";
      case PERIOD_H12: return "H12";
      case PERIOD_D1: return "D1";
      case PERIOD_W1: return "W1";
      case PERIOD_MN1: return "MN1";
   }
   return IntegerToString((int)tf);
}

void OnStart()
{
   string symbol = (InpSymbol == "" ? _Symbol : InpSymbol);
   if(!SymbolSelect(symbol, true))
   {
      Print("ExportRatesForAstroML: SymbolSelect failed: ", symbol);
      return;
   }

   MqlRates rates[];
   int copied = CopyRates(symbol, InpTimeframe, InpFrom, InpTo, rates);
   if(copied <= 0)
   {
      Print("ExportRatesForAstroML: CopyRates failed symbol=", symbol, " tf=", TFToString(InpTimeframe), " err=", GetLastError());
      return;
   }
   ArraySetAsSeries(rates, false);

   string out = InpOutputName;
   if(out == "")
      out = "astro_ml_prices_" + symbol + "_" + TFToString(InpTimeframe) + ".csv";

   int flags = FILE_WRITE | FILE_CSV | FILE_ANSI;
   if(InpUseCommonFiles)
      flags |= FILE_COMMON;
   int h = FileOpen(out, flags, ',');
   if(h == INVALID_HANDLE)
   {
      Print("ExportRatesForAstroML: FileOpen failed out=", out, " err=", GetLastError());
      return;
   }

   FileWrite(h, "broker_time", "symbol", "timeframe", "open", "high", "low", "close", "tick_volume", "spread", "real_volume");
   for(int i=0; i<copied; i++)
   {
      FileWrite(h,
                TimeToString(rates[i].time, TIME_DATE|TIME_MINUTES),
                symbol,
                TFToString(InpTimeframe),
                DoubleToString(rates[i].open, _Digits),
                DoubleToString(rates[i].high, _Digits),
                DoubleToString(rates[i].low, _Digits),
                DoubleToString(rates[i].close, _Digits),
                (long)rates[i].tick_volume,
                rates[i].spread,
                (long)rates[i].real_volume);
   }
   FileClose(h);
   Print("ExportRatesForAstroML: exported ", copied, " rows to Common\\Files\\", out);
}
