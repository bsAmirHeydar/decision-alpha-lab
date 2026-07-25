#property strict
#property version "1.00"
#property description "Strategy Factory Phase 08 candidate policy engine self-test"
#include <AlphaLab\StrategyFactory\Candidate\SF08_AllCandidate.mqh>
#include <AlphaLab\StrategyFactory\Testing\SF02_Assert.mqh>

bool BuildFixture(SF01_AnatomyEvent &event,CSF01FeatureSnapshot &snapshot,SF07_ContextFrame &frame,string &error)
{
   SF01_MarketTimestamp t=SF01_MakeUtcMilliseconds(1783771200000,"UTC",0,"fixture",SF01_TIME_MILLISECONDS);
   event.schema=SF01_AnatomyEventSchema();event.event_id="";event.strategy_id="sf08_fixture";event.strategy_version="1.0.0";event.producer_id="sf08.selftest";event.producer_version="1.0.0";event.symbol="EURUSD";event.reference_symbol="EURUSD";event.direction=SF01_DIRECTION_LONG;event.event_time=t;event.known_time=t;event.confirmation_time=t;event.reference_price=1.1000;event.invalidation_price=1.0980;event.timeframe_seconds=60;event.session_id="fixture";event.parent_event_id="none";event.market_event_cluster_id="cluster_sf08";event.source_hash="src_sf08";event.anatomy_state="confirmed";event.event_id=SF01_DeriveAnatomyEventId(event);if(!SF01_ValidateAnatomyEvent(event,error))return false;
   snapshot.schema=SF01_FeatureSnapshotSchema();snapshot.snapshot_id="";snapshot.event_id=event.event_id;snapshot.strategy_id=event.strategy_id;snapshot.snapshot_time=t;snapshot.producer_id="sf08.selftest";snapshot.producer_version="1.0.0";snapshot.source_hash="ctx_sf08";snapshot.state_generation=8;
   SF01_FeatureValue f=SF01_MakeDoubleFeature("confirmation_price","1.0.0",1.1010,t,event.event_id,"src_confirm");if(!snapshot.Add(f,error))return false;snapshot.snapshot_id=snapshot.DeriveId();if(!snapshot.Validate(error))return false;
   frame.schema="alpha_lab.strategy_factory/context_frame@1.0.0";frame.frame_id="";frame.event_id=event.event_id;frame.snapshot_id=snapshot.snapshot_id;frame.graph_hash="graph_sf08";frame.vector_schema_hash="vsch_sf08";frame.vector_id="fvec_sf08";frame.state_generation=8;frame.feature_count=1;frame.snapshot_time=t;frame.source_hash=event.source_hash;frame.frame_id=SF07_DeriveContextFrameId(frame);return SF07_ValidateContextFrame(frame,error);
}

int OnInit()
{
   CSF02Assert a;string e="";CSF08PolicyRegistry registry;CSF08FixturePolicyPack pack;CSF08CandidateMatrixPlan matrix;CSF08CandidateEngine engine;
   a.True(pack.RegisterAll(registry,e),"register fixture policies: "+e);a.True(registry.Compile(e),"compile policy registry: "+e);a.EqualInt(registry.EntryCount(),2,"entry policy count");a.EqualInt(registry.StopCount(),2,"stop policy count");a.EqualInt(registry.ExitCount(),2,"exit policy count");
   a.True(pack.BuildReferenceMatrix(matrix,e),"build reference matrix: "+e);a.True(matrix.Compile(registry,e),"compile matrix: "+e);a.EqualInt(matrix.Count(),2,"matrix template count");a.True(engine.Initialize(&registry,&matrix,16,SF08_QUEUE_FAIL_ENGINE,e),"initialize candidate engine: "+e);
   SF01_AnatomyEvent event;CSF01FeatureSnapshot snapshot;SF07_ContextFrame frame;a.True(BuildFixture(event,snapshot,frame,e),"build fixture: "+e);a.True(engine.BuildMatrix(event,snapshot,frame,8,e),"build candidate matrix: "+e);a.EqualInt(engine.Pending(),2,"candidate count");
   SF08_TradeCandidate c1,c2;a.True(engine.PopCandidate(c1),"pop first candidate");a.True(engine.PopCandidate(c2),"pop second candidate");a.True(c1.candidate_id!=c2.candidate_id,"candidate ids unique");a.True(SF08_ValidateTradeCandidate(c1,e),"first candidate valid: "+e);a.True(SF08_ValidateTradeCandidate(c2,e),"second candidate valid: "+e);a.True(c1.planned_r_multiple>0.0,"first candidate R positive");a.True(c2.planned_r_multiple>0.0,"second candidate R positive");
   SF08_CandidateTelemetry t=engine.Telemetry();a.EqualInt((int)t.candidates_emitted,2,"telemetry emitted count");a.EqualInt(engine.Pending(),0,"queue drained");
   if(!a.Passed()){Print("SF08 self-test FAILED: ",a.Summary());return INIT_FAILED;}Print("SF08 self-test PASS: ",a.Summary()," registry=",registry.RegistryHash()," matrix=",matrix.PlanHash());return INIT_SUCCEEDED;
}
