#ifndef __SF10_RESEARCH_HARNESS_MQH__
#define __SF10_RESEARCH_HARNESS_MQH__
#include "SF10_DifferentialComparator.mqh"
#include "SF10_ResearchTelemetry.mqh"

class CSF10ResearchHarness
{
private:
   bool m_ready;
   SF10_RunManifest m_manifest;
   SF10_ObjectiveConfig m_objective;
   CSF10ResearchAccumulator m_accumulator;
   SF10_ResearchTelemetry m_telemetry;
public:
   CSF10ResearchHarness(void){m_ready=false;ZeroMemory(m_telemetry);}
   bool Initialize(SF10_RunManifest manifest,const SF10_ObjectiveConfig &objective,const int max_unique,string &error)
   {
      manifest.manifest_hash=SF10_DeriveRunManifestHash(manifest);
      if(!SF10_ValidateRunManifest(manifest,error)){m_telemetry.manifest_failures++;return false;}
      m_manifest=manifest;m_objective=objective;m_accumulator.Reset(max_unique);m_ready=true;error="";return true;
   }
   bool ObserveOutcome(const SF09_OutcomeRecord &outcome,const string cluster_id,string &error)
   {
      if(!m_ready){error="research harness not initialized";return false;}
      if(!m_accumulator.Observe(outcome,cluster_id,error)){m_telemetry.outcomes_rejected++;return false;}
      m_telemetry.outcomes_observed++;return true;
   }
   SF10_PassSummary Finalize(const long public_id,const string parameter_hash,const bool emit_frame,string &error)
   {
      const ulong started=GetMicrosecondCount();
      SF10_PassSummary s;s.schema="alpha_lab.strategy_factory/optimization_pass_summary@1.0.0";s.public_id=public_id;
      s.run_id=m_manifest.run_id;s.manifest_hash=m_manifest.manifest_hash;s.parameter_hash=parameter_hash;
      s.metrics=m_accumulator.Snapshot();const SF10_ObjectiveResult o=SF10_EvaluateObjective(s.metrics,m_objective);
      s.objective_score=o.score;s.status=o.status;s.summary_hash="";s.summary_hash=SF10_DerivePassSummaryHash(s);
      if(emit_frame)
      {
         string frame_error="";
         if(SF10_SendOptimizationFrame(s,frame_error))m_telemetry.frames_sent++;
         else {m_telemetry.frame_failures++;error=frame_error;}
      }
      const long elapsed=(long)(GetMicrosecondCount()-started);m_telemetry.last_finalize_microseconds=elapsed;
      if(elapsed>m_telemetry.maximum_finalize_microseconds)m_telemetry.maximum_finalize_microseconds=elapsed;
      if(error=="")error=o.reason;return s;
   }
   SF10_ResearchMetrics Metrics(void) const{return m_accumulator.Snapshot();}
   SF10_RunManifest Manifest(void) const{return m_manifest;}
   SF10_ResearchTelemetry Telemetry(void) const{return m_telemetry;}
};
#endif
