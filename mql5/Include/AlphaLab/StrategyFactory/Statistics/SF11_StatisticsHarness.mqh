#ifndef __SF11_STATISTICS_HARNESS_MQH__
#define __SF11_STATISTICS_HARNESS_MQH__
#include "SF11_StatisticsExporter.mqh"
#include "SF11_StatisticsTelemetry.mqh"
class CSF11StatisticsHarness
{
private:CSF11GroupAccumulator m_all;SF11_StatisticsTelemetry m_telemetry;
public:
   CSF11StatisticsHarness(){Reset();}
   void Reset(void){m_all.Reset("all=all");ZeroMemory(m_telemetry);m_telemetry.groups_created=1;}
   bool Observe(const SF11_StatisticalSample &sample,string &error){if(!m_all.Observe(sample,error)){m_telemetry.samples_rejected++;return false;}m_telemetry.samples_observed++;return true;}
   SF11_StatisticSummary Finalize(const long minimum_samples=1){const ulong start=GetMicrosecondCount();SF11_StatisticSummary s=m_all.Snapshot(minimum_samples);m_telemetry.summaries_emitted++;m_telemetry.last_finalize_microseconds=(long)(GetMicrosecondCount()-start);if(m_telemetry.last_finalize_microseconds>m_telemetry.maximum_finalize_microseconds)m_telemetry.maximum_finalize_microseconds=m_telemetry.last_finalize_microseconds;return s;}
   SF11_StatisticsTelemetry Telemetry(void) const{return m_telemetry;}
};
#endif
