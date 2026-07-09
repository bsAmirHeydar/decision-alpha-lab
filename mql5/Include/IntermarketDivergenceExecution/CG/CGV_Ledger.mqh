#ifndef __CGV_LEDGER_MQH__
#define __CGV_LEDGER_MQH__

#include <IntermarketDivergenceExecution/CG/CGV_Types.mqh>
#include <IntermarketDivergenceExecution/CG/CGC_ConfirmationField.mqh>

class CCGV_Ledger
{
private:
   SCGVVisualLedgerConfig m_config;
   string m_memory_keys[];

   int FileFlags(const bool read_mode)
   {
      int flags=FILE_CSV|FILE_ANSI;
      if(read_mode)
         flags|=FILE_READ;
      else
         flags|=FILE_READ|FILE_WRITE;
      if(m_config.ledger_use_common_files)
         flags|=FILE_COMMON;
      return flags;
   }

   bool MemoryHasKey(const string key)
   {
      for(int i=0;i<ArraySize(m_memory_keys);i++)
      {
         if(m_memory_keys[i]==key)
            return true;
      }
      return false;
   }

   void AddMemoryKey(const string key)
   {
      if(MemoryHasKey(key))
         return;
      int n=ArraySize(m_memory_keys);
      ArrayResize(m_memory_keys,n+1);
      m_memory_keys[n]=key;
   }

   string DirectionText(SCGCFinalSignal &signal)
   {
      if(signal.direction==CGC_DIRECTION_BUY) return "BUY";
      if(signal.direction==CGC_DIRECTION_SELL) return "SELL";
      return "NONE";
   }

   string SideText(SCGCFinalSignal &signal)
   {
      if(signal.side==CGC_SIDE_HIGH) return "HIGH";
      if(signal.side==CGC_SIDE_LOW) return "LOW";
      return "NONE";
   }

   string StatusText(SCGCFinalSignal &signal)
   {
      if(signal.status==CGC_STATUS_CONFIRMED_TRADEABLE) return "CONFIRMED_TRADEABLE";
      if(signal.status==CGC_STATUS_INVALIDATED_DOUBLE_HUNT) return "INVALIDATED_DOUBLE_HUNT";
      if(signal.status==CGC_STATUS_MISSING_DATA) return "MISSING_DATA";
      return "NONE";
   }

   string BoolText(const bool v)
   {
      return v ? "true" : "false";
   }

   bool ShouldWrite(SCGCFinalSignal &signal)
   {
      if(!m_config.enable_ledger)
         return false;
      if(signal.status==CGC_STATUS_CONFIRMED_TRADEABLE && !m_config.write_confirmed_to_ledger)
         return false;
      if(signal.status==CGC_STATUS_INVALIDATED_DOUBLE_HUNT && !m_config.write_invalidated_to_ledger)
         return false;
      if(signal.status!=CGC_STATUS_CONFIRMED_TRADEABLE && signal.status!=CGC_STATUS_INVALIDATED_DOUBLE_HUNT)
         return false;
      return true;
   }

   bool ExistingFileHasKey(const string key)
   {
      if(!m_config.use_file_duplicate_guard)
         return false;
      int h=FileOpen(m_config.ledger_file_name,FileFlags(true),';');
      if(h==INVALID_HANDLE)
         return false;
      while(!FileIsEnding(h))
      {
         string first=FileReadString(h);
         if(first==key)
         {
            FileClose(h);
            return true;
         }
         for(int i=1;i<CGV_LEDGER_COLUMN_COUNT && !FileIsEnding(h);i++)
            FileReadString(h);
      }
      FileClose(h);
      return false;
   }

   void WriteHeaderIfEmpty(const int h)
   {
      if(FileSize(h)>0)
         return;
      FileWrite(h,
         "ledger_key","signal_id","status","direction","side","group_name","group_minutes","current_cycle_number","reference_cycle_number",
         "symbol_a","symbol_b","hunter_symbol","clean_symbol","symbol_a_is_hunter","symbol_b_is_hunter","one_sided_hunt","double_hunt_invalidated",
         "confirmation_time_broker","confirmation_time_utc","confirmation_time_ny","confirmation_timeframe",
         "trading_day_start_ny","trading_day_end_ny","current_cycle_start_ny","current_cycle_end_ny","reference_cycle_start_ny","reference_cycle_end_ny",
         "hunter_reference_price","clean_reference_price","hunter_current_extreme","clean_current_extreme","clean_stop_reference_price",
         "trade_permission_preview","data_ready","chart_symbol","phase","note","created_broker_time"
      );
   }

public:
   void Configure(SCGVVisualLedgerConfig &config)
   {
      m_config=config;
      ArrayResize(m_memory_keys,0);
   }

   string LedgerKey(SCGCFinalSignal &signal)
   {
      return signal.signal_id + "|" + StatusText(signal) + "|" + TimeToString(signal.confirmation_time_broker,TIME_DATE|TIME_MINUTES);
   }

   SCGVLedgerWriteResult AppendSignal(SCGCFinalSignal &signal)
   {
      SCGVLedgerWriteResult result;
      result.attempted=false;
      result.written=false;
      result.duplicate=false;
      result.error=false;
      result.message="";

      if(!ShouldWrite(signal))
      {
         result.message="not configured for this signal status";
         return result;
      }
      result.attempted=true;

      string key=LedgerKey(signal);
      if(MemoryHasKey(key) || ExistingFileHasKey(key))
      {
         result.duplicate=true;
         result.message="duplicate ledger key";
         AddMemoryKey(key);
         return result;
      }

      int h=FileOpen(m_config.ledger_file_name,FileFlags(false),';');
      if(h==INVALID_HANDLE)
      {
         result.error=true;
         result.message="FileOpen failed for ledger file";
         return result;
      }
      WriteHeaderIfEmpty(h);
      FileSeek(h,0,SEEK_END);
      FileWrite(h,
         key,signal.signal_id,StatusText(signal),DirectionText(signal),SideText(signal),signal.group_name,signal.group_minutes,signal.current_cycle_number,signal.reference_cycle_number,
         m_config.symbol_a,m_config.symbol_b,signal.hunter_symbol,signal.clean_symbol,BoolText(signal.symbol_a_is_hunter),BoolText(signal.symbol_b_is_hunter),BoolText(signal.one_sided_hunt),BoolText(signal.double_hunt_invalidated),
         TimeToString(signal.confirmation_time_broker,TIME_DATE|TIME_SECONDS),TimeToString(signal.confirmation_time_utc,TIME_DATE|TIME_SECONDS),TimeToString(signal.confirmation_time_ny,TIME_DATE|TIME_SECONDS),EnumToString(signal.confirmation_timeframe),
         TimeToString(signal.trading_day_start_ny,TIME_DATE|TIME_MINUTES),TimeToString(signal.trading_day_end_ny,TIME_DATE|TIME_MINUTES),TimeToString(signal.current_cycle_start_ny,TIME_DATE|TIME_MINUTES),TimeToString(signal.current_cycle_end_ny,TIME_DATE|TIME_MINUTES),TimeToString(signal.reference_cycle_start_ny,TIME_DATE|TIME_MINUTES),TimeToString(signal.reference_cycle_end_ny,TIME_DATE|TIME_MINUTES),
         DoubleToString(signal.hunter_reference_price,CGC_PRICE_DIGITS),DoubleToString(signal.clean_reference_price,CGC_PRICE_DIGITS),DoubleToString(signal.hunter_current_extreme,CGC_PRICE_DIGITS),DoubleToString(signal.clean_current_extreme,CGC_PRICE_DIGITS),DoubleToString(signal.clean_stop_reference_price,CGC_PRICE_DIGITS),
         BoolText(signal.trade_permission_preview),BoolText(signal.data_ready),_Symbol,"PHASE06_VISUAL_LEDGER",signal.note,TimeToString(TimeCurrent(),TIME_DATE|TIME_SECONDS)
      );
      FileClose(h);
      AddMemoryKey(key);
      result.written=true;
      result.message="written";
      return result;
   }
};

#endif
