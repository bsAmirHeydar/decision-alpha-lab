#ifndef __ISF05_VERSIONED_RESULT_SINK_MQH__
#define __ISF05_VERSIONED_RESULT_SINK_MQH__
#include "../Ports/ISF02_ResultSink.mqh"
#include "SF05_ResultEnvelope.mqh"

struct SF05_ResultSinkTelemetry
{
   long records_written;
   long events_written;
   long snapshots_written;
   long flush_count;
   long write_errors;
   long duplicate_rejections;
   long bytes_written;
   long last_sequence;
   long last_flush_utc_msc;
   string last_error;
};

class ISF05VersionedResultSink:public ISF02ResultSink
{
public:
   virtual bool Configure(const SF05_RunManifest &manifest,const SF05_RuntimeGenerationRecord &generation,const SF05_ResultSinkConfig &config,string &error)=0;
   virtual bool WriteEnvelope(SF05_ResultEnvelope &envelope,string &error)=0;
   virtual bool Seal(const SF01_MarketTimestamp &sealed_at,string &error)=0;
   virtual bool IsSealed(void)const=0;
   virtual SF05_ResultSinkTelemetry Telemetry(void)const=0;
};
#endif
