#ifndef __SF07_CONTEXT_ENGINE_MQH__
#define __SF07_CONTEXT_ENGINE_MQH__

#include "../Ports/ISF02_FeatureProvider.mqh"
#include "SF07_ContextFrame.mqh"
#include "SF07_ContextTelemetry.mqh"

class CSF07ContextEngine : public ISF02FeatureProvider
{
private:
   CSF07FeatureRegistry m_registry;
   CSF07ContextState m_state;
   CSF07FeatureVectorSchema m_vector_schema;
   CSF07FixedFeatureVector m_last_vector;
   SF07_ContextFrame m_last_frame;
   SF07_ContextTelemetry m_telemetry;
   bool m_initialized;
   bool m_started;
   bool m_vector_schema_configured;
   int m_context_capacity;
   ENUM_SF07_CONTEXT_STATUS m_status;

   bool ShouldRecompute(const SF07_FeatureDescriptor &descriptor,
                        const long snapshot_time_msc) const
   {
      if(descriptor.update_scope == SF07_UPDATE_EVENT) return true;
      if(m_state.IsDirty(descriptor.feature_id)) return true;
      return !m_state.IsFresh(descriptor.feature_id, snapshot_time_msc);
   }

   bool ValidateComputedValue(const SF07_FeatureDescriptor &descriptor,
                              const SF01_FeatureValue &value,
                              const SF01_MarketTimestamp &snapshot_time,
                              string &error) const
   {
      if(value.feature_id != descriptor.feature_id)
      { error = "feature node emitted unexpected feature id"; return false; }
      if(value.feature_version != descriptor.feature_version)
      { error = "feature node emitted unexpected version"; return false; }
      if(value.value_type != descriptor.value_type)
      { error = "feature node emitted unexpected type"; return false; }
      if(!SF01_ValidateFeatureValue(value, snapshot_time, error)) return false;
      if(descriptor.required && value.quality != SF01_QUALITY_VALID && value.quality != SF01_QUALITY_ESTIMATED)
      { error = "required feature is not valid: " + descriptor.feature_id; return false; }
      return true;
   }

public:
   CSF07ContextEngine(void)
   {
      m_initialized = false;
      m_started = false;
      m_vector_schema_configured = false;
      m_context_capacity = 256;
      m_status = SF07_CONTEXT_EMPTY;
      SF07_ResetContextTelemetry(m_telemetry);
   }

   string ServiceId(void) const { return "sf07.context_engine"; }
   ENUM_SF02_SERVICE_KIND ServiceKind(void) const { return SF02_SERVICE_FEATURES; }
   CSF07FeatureRegistry &Registry(void) { return m_registry; }
   ENUM_SF07_CONTEXT_STATUS Status(void) const { return m_status; }
   SF07_ContextTelemetry Telemetry(void) const { return m_telemetry; }
   SF07_ContextFrame LastFrame(void) const { return m_last_frame; }
   CSF07FixedFeatureVector LastVector(void) const { return m_last_vector; }

   void SetContextCapacity(const int capacity) { m_context_capacity = capacity; }

   bool ConfigureVectorSchema(const CSF07FeatureVectorSchema &schema, string &error)
   {
      m_vector_schema = schema;
      m_vector_schema_configured = true;
      error = "";
      return true;
   }

   bool Initialize(const SF02_RuntimeConfig &config, string &error)
   {
      m_status = SF07_CONTEXT_COMPILING;
      if(!m_state.Initialize(m_context_capacity, error))
      { m_status = SF07_CONTEXT_FAILED; return false; }
      if(!m_registry.Compile(error))
      { m_status = SF07_CONTEXT_FAILED; return false; }
      if(!m_vector_schema_configured)
      { error = "feature vector schema not configured"; m_status = SF07_CONTEXT_FAILED; return false; }
      if(!m_vector_schema.ValidateAgainst(m_registry, error))
      { m_status = SF07_CONTEXT_FAILED; return false; }
      m_initialized = true;
      m_status = SF07_CONTEXT_READY;
      error = "";
      return true;
   }

   bool Start(string &error)
   {
      if(!m_initialized)
      { error = "context engine not initialized"; return false; }
      m_started = true;
      m_status = SF07_CONTEXT_READY;
      error = "";
      return true;
   }

   void Stop(void) { m_started = false; }
   void Shutdown(void)
   {
      m_started = false;
      m_initialized = false;
      m_status = SF07_CONTEXT_EMPTY;
   }

   SF02_ServiceHealth Health(const long now_utc_msc) const
   {
      SF02_ServiceHealth health;
      health.service_id = ServiceId();
      health.service_kind = ServiceKind();
      health.observed_at_utc_msc = now_utc_msc;
      health.status = (m_initialized && m_started && m_status == SF07_CONTEXT_READY)
         ? SF02_HEALTH_HEALTHY : SF02_HEALTH_DEGRADED;
      health.detail = (health.status == SF02_HEALTH_HEALTHY) ? "running" : "not ready";
      return health;
   }

   bool BuildSnapshot(const SF01_AnatomyEvent &event,
                      const long state_generation,
                      CSF01FeatureSnapshot &snapshot,
                      string &error)
   {
      const ulong start_us = GetMicrosecondCount();
      if(!m_started)
      { error = "context engine not started"; return false; }
      m_status = SF07_CONTEXT_BUILDING;
      if(!m_state.BeginGeneration(state_generation, event.event_id, event.confirmation_time, error))
      { m_telemetry.build_failures++; m_status = SF07_CONTEXT_FAILED; return false; }
      m_state.MarkAllDirty(SF07_INVALIDATE_EVENT);

      snapshot.schema = SF01_FeatureSnapshotSchema();
      snapshot.snapshot_id = "";
      snapshot.event_id = event.event_id;
      snapshot.strategy_id = event.strategy_id;
      snapshot.snapshot_time = event.confirmation_time;
      snapshot.producer_id = ServiceId();
      snapshot.producer_version = "1.0.0";
      snapshot.source_hash = m_registry.GraphHash();
      snapshot.state_generation = state_generation;

      const int count = m_registry.Count();
      for(int position = 0; position < count; position++)
      {
         SF07_FeatureDescriptor descriptor;
         if(!m_registry.DescriptorAtTopological(position, descriptor))
         { error = "failed to read compiled feature descriptor"; m_telemetry.dependency_failures++; m_telemetry.build_failures++; m_status = SF07_CONTEXT_FAILED; return false; }
         SF01_FeatureValue feature;
         bool have_value = false;
         if(!ShouldRecompute(descriptor, snapshot.snapshot_time.utc_epoch_milliseconds))
         {
            have_value = m_state.Get(descriptor.feature_id, feature);
            if(have_value) m_telemetry.feature_cache_hits++;
         }
         if(!have_value)
         {
            ISF07FeatureNode *node = m_registry.NodeAtTopological(position);
            if(CheckPointer(node) == POINTER_INVALID)
            { error = "invalid compiled feature node"; m_telemetry.build_failures++; m_status = SF07_CONTEXT_FAILED; return false; }
            if(!node.Compute(event, m_state, feature, error))
            { m_telemetry.build_failures++; m_status = SF07_CONTEXT_FAILED; return false; }
            if(!ValidateComputedValue(descriptor, feature, snapshot.snapshot_time, error))
            { m_telemetry.build_failures++; m_status = SF07_CONTEXT_FAILED; return false; }
            if(!m_state.Put(feature, descriptor.max_age_milliseconds, error))
            { m_telemetry.build_failures++; m_status = SF07_CONTEXT_FAILED; return false; }
            m_telemetry.feature_computations++;
         }
         if(!snapshot.Add(feature, error))
         { m_telemetry.build_failures++; m_status = SF07_CONTEXT_FAILED; return false; }
      }

      snapshot.snapshot_id = snapshot.DeriveId();
      if(!snapshot.Validate(error))
      { m_telemetry.build_failures++; m_status = SF07_CONTEXT_FAILED; return false; }
      if(!m_last_vector.Build(m_vector_schema, snapshot, error))
      { m_telemetry.build_failures++; m_status = SF07_CONTEXT_FAILED; return false; }
      m_telemetry.vector_builds++;

      m_last_frame.schema = "alpha_lab.strategy_factory/context_frame@1.0.0";
      m_last_frame.frame_id = "";
      m_last_frame.event_id = event.event_id;
      m_last_frame.snapshot_id = snapshot.snapshot_id;
      m_last_frame.graph_hash = m_registry.GraphHash();
      m_last_frame.vector_schema_hash = m_vector_schema.Hash();
      m_last_frame.vector_id = m_last_vector.vector_id;
      m_last_frame.state_generation = state_generation;
      m_last_frame.feature_count = snapshot.Size();
      m_last_frame.snapshot_time = snapshot.snapshot_time;
      m_last_frame.source_hash = event.source_hash;
      m_last_frame.frame_id = SF07_DeriveContextFrameId(m_last_frame);
      if(!SF07_ValidateContextFrame(m_last_frame, error))
      { m_telemetry.build_failures++; m_status = SF07_CONTEXT_FAILED; return false; }

      const long elapsed = (long)(GetMicrosecondCount() - start_us);
      m_telemetry.build_count++;
      m_telemetry.total_build_microseconds += elapsed;
      if(elapsed > m_telemetry.maximum_build_microseconds) m_telemetry.maximum_build_microseconds = elapsed;
      m_status = SF07_CONTEXT_READY;
      error = "";
      return true;
   }
};

#endif
