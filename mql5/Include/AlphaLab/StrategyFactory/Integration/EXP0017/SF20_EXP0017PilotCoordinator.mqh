#ifndef __SF20_EXP0017_PILOT_COORDINATOR_MQH__
#define __SF20_EXP0017_PILOT_COORDINATOR_MQH__
#include "SF20_EXP0017PipelineBinding.mqh"
#include "../../Context/SF07_AllContext.mqh"
#include "../../Candidate/SF08_AllCandidate.mqh"
#include "../../Monitoring/SF19_AllMonitoring.mqh"
class CSF20EXP0017PilotCoordinator
{
private:CSF07ContextEngine m_context;CSF07FixtureFeaturePack m_features;CSF07FeatureVectorSchema m_vector_schema;CSF08PolicyRegistry m_policy_registry;CSF08FixturePolicyPack m_policy_pack;CSF08CandidateMatrixPlan m_matrix;CSF08CandidateEngine m_candidates;CSF19MonitoringCoordinator m_monitor;SF19_TelemetrySchemaEntry m_schema;SF02_RuntimeConfig m_runtime;long m_generation,m_sequence;bool m_ready;
public:CSF20EXP0017PilotCoordinator(){m_generation=1;m_sequence=0;m_ready=false;}
 bool Configure(const SF02_RuntimeConfig &runtime,string &error)
 {
  m_runtime=runtime;if(!m_features.RegisterAll(m_context.Registry(),error)||!m_features.BuildDefaultVectorSchema(m_vector_schema,error)||!m_context.ConfigureVectorSchema(m_vector_schema,error)||!m_context.Initialize(runtime,error)||!m_context.Start(error))return false;
  if(!m_policy_pack.RegisterAll(m_policy_registry,error)||!m_policy_registry.Compile(error)||!m_policy_pack.BuildReferenceMatrix(m_matrix,error)||!m_matrix.Compile(m_policy_registry,error)||!m_candidates.Initialize(&m_policy_registry,&m_matrix,64,SF08_QUEUE_FAIL_ENGINE,error))return false;
  if(!m_monitor.Configure(runtime.run_id,"sf20-pilot-generation",runtime.strategy_id,"no_exp0017_model",1024,error))return false;
  m_schema.metric_name="integration.exp0017.event_count";m_schema.schema_version="1.0.0";m_schema.metric_kind=SF19_METRIC_COUNTER;m_schema.unit="count";m_schema.stage="integration";m_schema.description="EXP0017 canonical events accepted by pilot";m_schema.has_lower_bound=true;m_schema.lower_bound=0.0;m_schema.has_upper_bound=false;m_schema.upper_bound=0.0;m_schema.schema_id=SF19_DeriveSchemaId(m_schema);m_ready=true;error="";return true;
 }
 bool Route(const SF01_AnatomyEvent &event,SF20_EXP0017StageEvidence &stages[],int &candidate_count,string &error)
 {
  candidate_count=0;if(!m_ready){error="pilot coordinator not ready";return false;}CSF01FeatureSnapshot snapshot;if(!m_context.BuildSnapshot(event,m_generation++,snapshot,error))return false;SF07_ContextFrame frame=m_context.LastFrame();if(!m_candidates.BuildMatrix(event,snapshot,frame,m_generation,error))return false;string candidate_ids="";SF08_TradeCandidate candidate;while(m_candidates.PopCandidate(candidate)){candidate_count++;candidate_ids+=(candidate_ids==""?"":"|")+candidate.candidate_id;}
  SF20_BuildFailClosedPilotRoute(event,frame.frame_id,candidate_ids,event.known_time.utc_epoch_milliseconds,stages);m_sequence++;SF19_TelemetryEvent telemetry;telemetry.metric_name=m_schema.metric_name;telemetry.schema_id=m_schema.schema_id;telemetry.run_id=m_runtime.run_id;telemetry.generation_id="sf20-pilot-generation";telemetry.strategy_id=m_runtime.strategy_id;telemetry.model_id="no_exp0017_model";telemetry.correlation_id=event.event_id;telemetry.causation_id=event.parent_event_id;telemetry.observed_time_utc_msc=event.event_time.utc_epoch_milliseconds;telemetry.known_time_utc_msc=event.known_time.utc_epoch_milliseconds;telemetry.sequence=m_sequence;telemetry.value=1.0;telemetry.payload_hash=SF19_DeriveTelemetryPayloadHash(telemetry);telemetry.event_id=SF19_DeriveTelemetryEventId(telemetry);if(!m_monitor.Ingest(m_schema,telemetry,error))return false;error="";return true;
 }
 int MonitoringCount()const{return m_monitor.TelemetryCount();}
};
#endif
