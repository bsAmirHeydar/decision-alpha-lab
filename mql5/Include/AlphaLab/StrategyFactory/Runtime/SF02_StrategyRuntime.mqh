#ifndef __SF02_STRATEGY_RUNTIME_MQH__
#define __SF02_STRATEGY_RUNTIME_MQH__

#include "../Core/SF02_AllCore.mqh"
#include "../Ports/SF02_AllPorts.mqh"
#include "SF02_ServiceRegistry.mqh"

class CSF02StrategyRuntime
{
private:
   SF02_RuntimeConfig m_config;
   CSF02RuntimeStateMachine m_state;
   CSF02TypedEventBus m_audit_bus;
   CSF02ServiceRegistry m_registry;

   ISF02ClockPort *m_clock;
   ISF02AnatomyProvider *m_anatomy;
   ISF02FeatureProvider *m_features;
   ISF02ResultSink *m_sink;
   ISF02ExecutionBoundary *m_execution_boundary;

   long m_processed_events;
   long m_rejected_events;
   long m_created_snapshots;
   string m_last_error;

   bool PublishAudit(const ENUM_SF02_EVENT_TYPE event_type,
                     const string aggregate_id,
                     const string source_id,
                     const SF01_MarketTimestamp &occurred_at,
                     const SF01_MarketTimestamp &known_at,
                     const string payload_hash,
                     const int priority)
   {
      if(!m_config.enable_audit_bus) return true;
      SF02_EventEnvelope envelope;
      envelope.sequence = 0;
      envelope.event_type = event_type;
      envelope.aggregate_id = aggregate_id;
      envelope.source_id = source_id;
      envelope.occurred_at = occurred_at;
      envelope.known_at = known_at;
      envelope.payload_hash = payload_hash;
      envelope.priority = priority;
      string error = "";
      const bool ok = m_audit_bus.Publish(envelope, error);
      if(!ok) m_last_error = error;
      return ok;
   }

   bool Fail(const string reason)
   {
      m_last_error = reason;
      string ignored = "";
      const long now = (CheckPointer(m_clock) == POINTER_INVALID) ? 0 : m_clock.UtcNowMilliseconds();
      if(m_state.State() != SF02_STATE_FAILED)
         m_state.Transition(SF02_STATE_FAILED, now, reason, ignored);
      return false;
   }

   bool RegisterBoundServices(string &error)
   {
      if(!m_registry.Register(m_clock, error)) return false;
      if(!m_registry.Register(m_anatomy, error)) return false;
      if(!m_registry.Register(m_features, error)) return false;
      if(!m_registry.Register(m_sink, error)) return false;
      if(CheckPointer(m_execution_boundary) != POINTER_INVALID)
      {
         if(!m_registry.Register(m_execution_boundary, error)) return false;
      }
      return true;
   }

   bool InitializeServices(string &error)
   {
      const int count = m_registry.Count();
      for(int i = 0; i < count; i++)
      {
         ISF02LifecycleService *service = m_registry.At(i);
         if(CheckPointer(service) == POINTER_INVALID)
         { error = "service registry contains invalid pointer"; return false; }
         if(!service.Initialize(m_config, error))
         { error = service.ServiceId() + ": " + error; return false; }
      }
      return true;
   }

   bool StartServices(string &error)
   {
      const int count = m_registry.Count();
      for(int i = 0; i < count; i++)
      {
         ISF02LifecycleService *service = m_registry.At(i);
         if(!service.Start(error))
         { error = service.ServiceId() + ": " + error; return false; }
      }
      return true;
   }

   bool DrainEvents(string &error)
   {
      int processed_this_cycle = 0;
      while(processed_this_cycle < m_config.max_events_per_cycle)
      {
         SF01_AnatomyEvent event;
         if(!m_anatomy.PopEvent(event)) break;
         processed_this_cycle++;

         string validation_error = "";
         if(!SF01_ValidateAnatomyEvent(event, validation_error))
         {
            m_rejected_events++;
            PublishAudit(SF02_EVENT_ANATOMY_REJECTED,
                         event.event_id == "" ? "invalid_event" : event.event_id,
                         m_anatomy.ServiceId(),
                         event.event_time,
                         event.known_time,
                         event.source_hash == "" ? "invalid_hash" : event.source_hash,
                         90);
            if(m_config.strict_fail_closed)
            { error = "invalid anatomy event: " + validation_error; return false; }
            continue;
         }

         if(event.event_id == "") event.event_id = SF01_DeriveAnatomyEventId(event);
         if(!m_sink.WriteEvent(event, validation_error))
         { error = "event sink failed: " + validation_error; return false; }
         m_processed_events++;
         PublishAudit(SF02_EVENT_ANATOMY_DETECTED,
                      event.event_id,
                      m_anatomy.ServiceId(),
                      event.event_time,
                      event.known_time,
                      event.source_hash,
                      50);

         CSF01FeatureSnapshot snapshot;
         if(!m_features.BuildSnapshot(event,
                                      m_config.generation_id,
                                      snapshot,
                                      validation_error))
         {
            PublishAudit(SF02_EVENT_SNAPSHOT_REJECTED,
                         event.event_id,
                         m_features.ServiceId(),
                         event.known_time,
                         event.confirmation_time,
                         event.source_hash,
                         90);
            if(m_config.strict_fail_closed)
            { error = "feature snapshot build failed: " + validation_error; return false; }
            continue;
         }

         if(snapshot.snapshot_id == "") snapshot.snapshot_id = snapshot.DeriveId();
         if(!snapshot.Validate(validation_error))
         {
            if(m_config.strict_fail_closed)
            { error = "invalid feature snapshot: " + validation_error; return false; }
            continue;
         }
         if(!m_sink.WriteSnapshot(snapshot, validation_error))
         { error = "snapshot sink failed: " + validation_error; return false; }
         m_created_snapshots++;
         PublishAudit(SF02_EVENT_SNAPSHOT_CREATED,
                      snapshot.snapshot_id,
                      m_features.ServiceId(),
                      snapshot.snapshot_time,
                      snapshot.snapshot_time,
                      snapshot.source_hash,
                      50);
      }
      error = "";
      return true;
   }

public:
   CSF02StrategyRuntime(void)
   {
      m_clock = NULL;
      m_anatomy = NULL;
      m_features = NULL;
      m_sink = NULL;
      m_execution_boundary = NULL;
      m_processed_events = 0;
      m_rejected_events = 0;
      m_created_snapshots = 0;
      m_last_error = "";
   }

   void BindClock(ISF02ClockPort *value) { m_clock = value; }
   void BindAnatomy(ISF02AnatomyProvider *value) { m_anatomy = value; }
   void BindFeatures(ISF02FeatureProvider *value) { m_features = value; }
   void BindSink(ISF02ResultSink *value) { m_sink = value; }
   void BindExecutionBoundary(ISF02ExecutionBoundary *value) { m_execution_boundary = value; }

   ENUM_SF02_RUNTIME_STATE State(void) const { return m_state.State(); }
   long ProcessedEvents(void) const { return m_processed_events; }
   long RejectedEvents(void) const { return m_rejected_events; }
   long CreatedSnapshots(void) const { return m_created_snapshots; }
   long DroppedAuditEvents(void) const { return m_audit_bus.Dropped(); }
   string LastError(void) const { return m_last_error; }

   bool Initialize(const SF02_RuntimeConfig &config, string &error)
   {
      m_config = config;
      if(!SF02_ValidateRuntimeConfig(m_config, error)) return Fail(error);
      if(CheckPointer(m_clock) == POINTER_INVALID ||
         CheckPointer(m_anatomy) == POINTER_INVALID ||
         CheckPointer(m_features) == POINTER_INVALID ||
         CheckPointer(m_sink) == POINTER_INVALID)
      { error = "required runtime port not bound"; return Fail(error); }

      if(m_config.run_mode == SF02_MODE_LIVE_DISABLED)
      {
         if(CheckPointer(m_execution_boundary) == POINTER_INVALID)
         { error = "live-disabled mode requires explicit execution boundary"; return Fail(error); }
         if(m_execution_boundary.HasLiveOrderAuthority())
         { error = "phase 02 forbids live order authority"; return Fail(error); }
      }

      const long now = m_clock.UtcNowMilliseconds();
      if(!m_state.Transition(SF02_STATE_INITIALIZING, now, "initialize", error)) return Fail(error);
      if(!m_audit_bus.Initialize(m_config.audit_bus_capacity,
                                 m_config.audit_overflow_policy,
                                 error)) return Fail(error);
      if(!RegisterBoundServices(error)) return Fail(error);
      if(!InitializeServices(error)) return Fail(error);
      if(!m_state.Transition(SF02_STATE_READY, m_clock.UtcNowMilliseconds(), "ready", error)) return Fail(error);
      return true;
   }

   bool Start(string &error)
   {
      if(m_state.State() != SF02_STATE_READY)
      { error = "runtime is not READY"; return false; }
      if(!StartServices(error)) return Fail(error);
      if(!m_state.Transition(SF02_STATE_RUNNING, m_clock.UtcNowMilliseconds(), "running", error)) return Fail(error);
      return true;
   }

   bool OnTick(const MqlTick &tick, string &error)
   {
      if(m_state.State() != SF02_STATE_RUNNING && m_state.State() != SF02_STATE_DEGRADED)
      { error = "runtime is not running"; return false; }
      m_anatomy.ProcessTick(tick);
      if(!DrainEvents(error)) return Fail(error);
      return true;
   }

   bool OnTimer(string &error)
   {
      if(m_state.State() != SF02_STATE_RUNNING && m_state.State() != SF02_STATE_DEGRADED)
      { error = "runtime is not running"; return false; }
      const long now = m_clock.UtcNowMilliseconds();
      m_anatomy.ProcessTimer(now);
      if(!DrainEvents(error)) return Fail(error);
      if(!m_sink.Flush(error)) return Fail(error);
      return true;
   }

   bool Stop(string &error)
   {
      if(m_state.State() == SF02_STATE_STOPPED) { error = ""; return true; }
      if(m_state.State() != SF02_STATE_RUNNING &&
         m_state.State() != SF02_STATE_DEGRADED &&
         m_state.State() != SF02_STATE_READY)
      { error = "runtime cannot stop from current state"; return false; }
      if(!m_state.Transition(SF02_STATE_STOPPING, m_clock.UtcNowMilliseconds(), "stopping", error)) return false;
      const int count = m_registry.Count();
      for(int i = count - 1; i >= 0; i--)
      {
         ISF02LifecycleService *service = m_registry.At(i);
         if(CheckPointer(service) != POINTER_INVALID) service.Stop();
      }
      if(!m_state.Transition(SF02_STATE_STOPPED, m_clock.UtcNowMilliseconds(), "stopped", error)) return false;
      return true;
   }

   void Shutdown(void)
   {
      const int count = m_registry.Count();
      for(int i = count - 1; i >= 0; i--)
      {
         ISF02LifecycleService *service = m_registry.At(i);
         if(CheckPointer(service) != POINTER_INVALID) service.Shutdown();
      }
   }

   bool PollAudit(SF02_EventEnvelope &event) { return m_audit_bus.Poll(event); }
};

#endif
