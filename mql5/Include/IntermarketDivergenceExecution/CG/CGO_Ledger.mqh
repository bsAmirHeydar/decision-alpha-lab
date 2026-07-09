#ifndef __CGO_LEDGER_MQH__
#define __CGO_LEDGER_MQH__

#include <IntermarketDivergenceExecution/CG/CGO_Types.mqh>

class CCGO_OutcomeLedger
{
private:
   SCGOOutcomeConfig m_config;
   string m_written_keys[];

   bool HasKey(const string key)
   {
      for(int i=0;i<ArraySize(m_written_keys);i++)
         if(m_written_keys[i]==key) return true;
      return false;
   }

   void AddKey(const string key)
   {
      int n=ArraySize(m_written_keys);
      ArrayResize(m_written_keys,n+1);
      m_written_keys[n]=key;
   }

   string DirectionText(const ECGCSignalDirection direction)
   {
      if(direction==CGC_DIRECTION_BUY) return "BUY";
      if(direction==CGC_DIRECTION_SELL) return "SELL";
      return "NONE";
   }

   string SideText(const ECGCSignalSide side)
   {
      if(side==CGC_SIDE_HIGH) return "HIGH";
      if(side==CGC_SIDE_LOW) return "LOW";
      return "NONE";
   }

   string AvailabilityText(const ECGOOutcomeAvailability availability)
   {
      if(availability==CGO_OUTCOME_COMPLETE) return "COMPLETE";
      if(availability==CGO_OUTCOME_PENDING_FUTURE) return "PENDING_FUTURE";
      if(availability==CGO_OUTCOME_MISSING_DATA) return "MISSING_DATA";
      if(availability==CGO_OUTCOME_ZERO_RISK) return "ZERO_RISK";
      return "UNAVAILABLE";
   }

   string T(const datetime t)
   {
      if(t<=0) return "";
      return TimeToString(t,TIME_DATE|TIME_MINUTES|TIME_SECONDS);
   }

   int Flags()
   {
      int flags=FILE_CSV|FILE_ANSI|FILE_READ|FILE_WRITE;
      if(m_config.ledger_use_common_files) flags|=FILE_COMMON;
      return flags;
   }

public:
   void Configure(SCGOOutcomeConfig &config)
   {
      m_config=config;
      ArrayResize(m_written_keys,0);
   }

   bool ResetFileIfNeeded()
   {
      if(!m_config.enable_ledger || !m_config.clear_ledger_on_init)
         return true;
      int h=FileOpen(m_config.ledger_file_name,Flags(),',');
      if(h==INVALID_HANDLE) return false;
      FileClose(h);
      FileDelete(m_config.ledger_file_name,(m_config.ledger_use_common_files ? FILE_COMMON : 0));
      return true;
   }

   bool EnsureHeader()
   {
      if(!m_config.enable_ledger) return true;
      bool exists=FileIsExist(m_config.ledger_file_name,(m_config.ledger_use_common_files ? FILE_COMMON : 0));
      int h=FileOpen(m_config.ledger_file_name,Flags(),',');
      if(h==INVALID_HANDLE) return false;
      if(!exists || FileSize(h)==0)
      {
         FileWrite(h,
            "outcome_id","signal_id","availability","availability_note","group","group_minutes","current_cycle","reference_cycle",
            "direction","side","clean_symbol","hunter_symbol","confirmation_broker","confirmation_ny","entry_broker","entry_price","stop_price","stop_points",
            "cycle_end_broker","cycle_end_price","cycle_end_points","cycle_end_r","cycle_stop_hit",
            "plus1_broker","plus1_price","plus1_points","plus1_r","plus2_broker","plus2_price","plus2_points","plus2_r","plus3_broker","plus3_price","plus3_points","plus3_r",
            "day_end_broker","day_end_price","day_end_points","day_end_r","mfe_price","mfe_points","mfe_r","mae_price","mae_points","mae_r","stop_hit_intraday","stop_hit_time","daily_range_points","day_end_norm_daily_range","mfe_norm_daily_range","note");
      }
      FileClose(h);
      return true;
   }

   bool WriteRow(SCGOOutcomeRow &row,bool &duplicate)
   {
      duplicate=false;
      if(!m_config.enable_ledger)
         return true;
      if(m_config.use_in_memory_duplicate_guard && HasKey(row.outcome_id))
      {
         duplicate=true;
         return false;
      }
      EnsureHeader();
      int h=FileOpen(m_config.ledger_file_name,Flags(),',');
      if(h==INVALID_HANDLE) return false;
      FileSeek(h,0,SEEK_END);
      FileWrite(h,
         row.outcome_id,row.signal_id,AvailabilityText(row.availability),row.availability_note,row.group_name,row.group_minutes,row.current_cycle_number,row.reference_cycle_number,
         DirectionText(row.direction),SideText(row.side),row.clean_symbol,row.hunter_symbol,T(row.confirmation_time_broker),T(row.confirmation_time_ny),T(row.entry_time_broker),row.entry_price,row.stop_price,row.stop_distance_points,
         T(row.cycle_end_time_broker),row.cycle_end_price,row.cycle_end_points,row.cycle_end_r,(row.cycle_end_stop_hit?"true":"false"),
         T(row.plus1_time_broker),row.plus1_price,row.plus1_points,row.plus1_r,T(row.plus2_time_broker),row.plus2_price,row.plus2_points,row.plus2_r,T(row.plus3_time_broker),row.plus3_price,row.plus3_points,row.plus3_r,
         T(row.day_end_time_broker),row.day_end_price,row.day_end_points,row.day_end_r,row.mfe_price,row.mfe_points,row.mfe_r,row.mae_price,row.mae_points,row.mae_r,(row.stop_hit_intraday?"true":"false"),T(row.stop_hit_time_broker),row.daily_range_points,row.day_end_normalized_by_daily_range,row.mfe_normalized_by_daily_range,row.note);
      FileClose(h);
      if(m_config.use_in_memory_duplicate_guard) AddKey(row.outcome_id);
      return true;
   }
};

#endif
