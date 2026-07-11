#property strict
#property description "Phase 19 observability host. No order or model mutation authority."
#include <AlphaLab/StrategyFactory/Monitoring/SF19_AllMonitoring.mqh>
input bool InpMonitoringEnabled=true;
input int InpTelemetryRingCapacity=1024;
input int InpSnapshotIntervalSeconds=60;
CSF19MonitoringCoordinator g_monitor;long g_sequence=0;SF19_TelemetrySchemaEntry g_queue_schema;
int OnInit(){if(!InpMonitoringEnabled)return INIT_SUCCEEDED;string error;SF19_BuildReferenceSchema("runtime.queue_depth",SF19_METRIC_GAUGE,"count","runtime",g_queue_schema);if(!g_monitor.Configure("sf19-runtime","generation-runtime","strategy-runtime","model-runtime",InpTelemetryRingCapacity,error)){Print(error);return INIT_FAILED;}SF19_AlertPolicy p;SF19_BuildReferenceAlertPolicy(p);if(!g_monitor.AddAlertPolicy(p,error)){Print(error);return INIT_FAILED;}EventSetTimer(MathMax(1,InpSnapshotIntervalSeconds));return INIT_SUCCEEDED;}
void OnDeinit(const int reason){EventKillTimer();}
void OnTimer(){if(!InpMonitoringEnabled)return;long now=(long)TimeCurrent()*1000;g_sequence++;SF19_TelemetryEvent e;SF19_BuildReferenceEvent(g_queue_schema,g_sequence,now,0.0,e);e.run_id="sf19-runtime";e.generation_id="generation-runtime";e.strategy_id="strategy-runtime";e.model_id="model-runtime";e.payload_hash=SF19_DeriveTelemetryPayloadHash(e);e.event_id=SF19_DeriveTelemetryEventId(e);string error;if(!g_monitor.Ingest(g_queue_schema,e,error))Print("SF19 ingest: ",error);SF19_HealthSnapshot h;SF19_LifecycleRecommendation r;g_monitor.Snapshot(now,h,r);Print("SF19 health=",IntegerToString((int)h.state)," action=",IntegerToString((int)r.action)," approval=",SF01_CanonicalBool(r.requires_operator_approval));}
void OnTick(){}
