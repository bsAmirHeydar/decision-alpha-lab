#ifndef __SF13_DATASET_EXPORTER_MQH__
#define __SF13_DATASET_EXPORTER_MQH__
#include "SF13_DatasetAssembler.mqh"
class CSF13DatasetCsvExporter
{
public:
   bool Export(const string relative_path,const CSF13DatasetAssembler &assembler,string &error)const
   {
      int handle=FileOpen(relative_path,FILE_WRITE|FILE_CSV|FILE_ANSI|FILE_COMMON,',');if(handle==INVALID_HANDLE){error="cannot open dataset CSV";return false;}
      FileWrite(handle,"row_id","fold_id","role","event_id","cluster_id","candidate_id","outcome_id","known_time_utc_msc","decision_time_utc_msc","resolved_time_utc_msc","label_available","label_value","row_hash");
      for(int i=0;i<assembler.Count();i++){SF13_DatasetRow row;if(!assembler.Get(i,row)){FileClose(handle);error="dataset assembler read failed";return false;}FileWrite(handle,row.row_id,row.fold_id,IntegerToString((int)row.role),row.event_id,row.cluster_id,row.candidate_id,row.outcome_id,IntegerToString(row.known_time_utc_msc),IntegerToString(row.decision_time_utc_msc),IntegerToString(row.resolved_time_utc_msc),SF01_CanonicalBool(row.label_available),(row.label_available?SF01_CanonicalDouble(row.label_value,10):"NA"),row.row_hash);}
      FileClose(handle);error="";return true;
   }
};
#endif
