#ifndef __SF08_CANDIDATE_ENGINE_MQH__
#define __SF08_CANDIDATE_ENGINE_MQH__
#include "SF08_CandidateMatrixPlan.mqh"
#include "SF08_CandidateQueue.mqh"
#include "SF08_CandidateTelemetry.mqh"

class CSF08CandidateEngine
{
private:
   CSF08PolicyRegistry *m_registry;
   CSF08CandidateMatrixPlan *m_plan;
   CSF08CandidateQueue m_queue;
   SF08_CandidateTelemetry m_telemetry;
   bool m_initialized;

   bool ContextMatches(const SF01_AnatomyEvent &event,const CSF01FeatureSnapshot &snapshot,const SF07_ContextFrame &frame,string &error)const
   {
      if(snapshot.event_id!=event.event_id || frame.event_id!=event.event_id || frame.snapshot_id!=snapshot.snapshot_id)
      {error="event, snapshot and context frame mismatch";return false;}
      if(snapshot.snapshot_time.utc_epoch_milliseconds<event.known_time.utc_epoch_milliseconds)
      {error="snapshot precedes event known time";return false;}
      if(frame.state_generation!=snapshot.state_generation)
      {error="context generation mismatch";return false;}
      return true;
   }

   bool BuildOne(const SF08_CandidateTemplate &t,
                 const SF01_AnatomyEvent &event,
                 const CSF01FeatureSnapshot &snapshot,
                 const SF07_ContextFrame &frame,
                 const long runtime_generation,
                 SF08_TradeCandidate &candidate,
                 ENUM_SF08_SKIP_REASON &skip_reason,
                 string &error)
   {
      ISF08EntryPolicy *entry_policy=m_registry.ResolveEntry(t.entry_policy_id,t.entry_policy_version);
      ISF08StopPolicy *stop_policy=m_registry.ResolveStop(t.stop_policy_id,t.stop_policy_version);
      ISF08ExitPolicy *exit_policy=m_registry.ResolveExit(t.exit_policy_id,t.exit_policy_version);
      if(CheckPointer(entry_policy)==POINTER_INVALID || CheckPointer(stop_policy)==POINTER_INVALID || CheckPointer(exit_policy)==POINTER_INVALID)
      {skip_reason=SF08_SKIP_POLICY_NOT_FOUND;error="template policy not resolved";return false;}
      string reason="";ENUM_SF08_POLICY_DECISION d=entry_policy.EvaluateAdmissibility(event,snapshot,frame,t.entry_parameters,reason);
      if(d==SF08_POLICY_SKIP){skip_reason=SF08_SKIP_ENTRY_INADMISSIBLE;error=reason;return false;} if(d==SF08_POLICY_ERROR){skip_reason=SF08_SKIP_POLICY_ERROR;error=reason;return false;}
      d=stop_policy.EvaluateAdmissibility(event,snapshot,frame,t.stop_parameters,reason);
      if(d==SF08_POLICY_SKIP){skip_reason=SF08_SKIP_STOP_INADMISSIBLE;error=reason;return false;} if(d==SF08_POLICY_ERROR){skip_reason=SF08_SKIP_POLICY_ERROR;error=reason;return false;}
      d=exit_policy.EvaluateAdmissibility(event,snapshot,frame,t.exit_parameters,reason);
      if(d==SF08_POLICY_SKIP){skip_reason=SF08_SKIP_EXIT_INADMISSIBLE;error=reason;return false;} if(d==SF08_POLICY_ERROR){skip_reason=SF08_SKIP_POLICY_ERROR;error=reason;return false;}
      SF08_EntryPlan entry;SF08_StopPlan stop;SF08_ExitPlan exit_plan;
      if(!entry_policy.Build(event,snapshot,frame,t.entry_parameters,entry,error) || !stop_policy.Build(event,snapshot,frame,t.stop_parameters,stop,error) || !exit_policy.Build(event,snapshot,frame,t.exit_parameters,exit_plan,error))
      {skip_reason=SF08_SKIP_POLICY_ERROR;return false;}
      candidate.schema="alpha_lab.strategy_factory/trade_candidate@1.0.0";candidate.candidate_id="";candidate.template_id=t.template_id;candidate.template_hash=t.template_hash;candidate.event_id=event.event_id;candidate.snapshot_id=snapshot.snapshot_id;candidate.context_frame_id=frame.frame_id;candidate.strategy_id=event.strategy_id;candidate.strategy_version=event.strategy_version;candidate.symbol=event.symbol;candidate.direction=event.direction;candidate.runtime_generation_id=runtime_generation;candidate.created_at=snapshot.snapshot_time;candidate.entry=entry;candidate.stop=stop;candidate.exit_plan=exit_plan;candidate.planned_r_multiple=exit_plan.planned_reward_points/stop.initial_risk_points;candidate.source_hash=SF01_StableId("csrc",event.source_hash+"|"+frame.frame_id+"|"+t.template_hash);candidate.status=SF08_CANDIDATE_VALID;candidate.candidate_id=SF08_DeriveTradeCandidateId(candidate);
      if(!SF08_ValidateTradeCandidate(candidate,error)){skip_reason=SF08_SKIP_GEOMETRY_INVALID;return false;}
      skip_reason=SF08_SKIP_NONE;error="";return true;
   }
public:
   CSF08CandidateEngine(void){m_registry=NULL;m_plan=NULL;m_initialized=false;SF08_ResetCandidateTelemetry(m_telemetry);}
   bool Initialize(CSF08PolicyRegistry *registry,CSF08CandidateMatrixPlan *plan,const int queue_capacity,const ENUM_SF08_QUEUE_OVERFLOW_POLICY overflow,string &error)
   {
      if(CheckPointer(registry)==POINTER_INVALID||CheckPointer(plan)==POINTER_INVALID){error="candidate engine dependencies missing";return false;}
      if(!registry.Compiled()||!plan.Compiled()){error="candidate engine dependencies not compiled";return false;}
      if(!m_queue.Configure(queue_capacity,overflow,error))return false;m_registry=registry;m_plan=plan;m_initialized=true;SF08_ResetCandidateTelemetry(m_telemetry);error="";return true;
   }
   SF08_CandidateTelemetry Telemetry(void)const{return m_telemetry;} int Pending(void)const{return m_queue.Count();}
   bool BuildMatrix(const SF01_AnatomyEvent &event,const CSF01FeatureSnapshot &snapshot,const SF07_ContextFrame &frame,const long runtime_generation,string &error)
   {
      const ulong started=GetMicrosecondCount();m_telemetry.build_requests++;
      if(!m_initialized){error="candidate engine not initialized";return false;}
      if(!ContextMatches(event,snapshot,frame,error))return false;
      m_queue.Clear();
      for(int i=0;i<m_plan.Count();i++)
      {
         SF08_CandidateTemplate t;if(!m_plan.At(i,t)){error="candidate template read failure";return false;}m_telemetry.templates_considered++;
         if(!t.enabled){m_telemetry.templates_disabled++;continue;}
         SF08_TradeCandidate candidate;ENUM_SF08_SKIP_REASON skip_reason=SF08_SKIP_NONE;string local="";
         if(!BuildOne(t,event,snapshot,frame,runtime_generation,candidate,skip_reason,local))
         {
            if(skip_reason==SF08_SKIP_POLICY_ERROR){m_telemetry.policy_errors++;error=local;return false;}
            if(skip_reason==SF08_SKIP_GEOMETRY_INVALID)m_telemetry.geometry_rejections++;else m_telemetry.policy_skips++;
            continue;
         }
         if(m_queue.Contains(candidate.candidate_id)){m_telemetry.duplicates_rejected++;continue;}
         if(!m_queue.Push(candidate,local)){m_telemetry.queue_overflows++;error=local;return false;}
         m_telemetry.candidates_emitted++;
      }
      const long elapsed=(long)(GetMicrosecondCount()-started);m_telemetry.total_build_microseconds+=elapsed;if(elapsed>m_telemetry.maximum_build_microseconds)m_telemetry.maximum_build_microseconds=elapsed;error="";return true;
   }
   bool PopCandidate(SF08_TradeCandidate &candidate){return m_queue.Pop(candidate);}
};

#endif
