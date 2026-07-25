"""Synthetic and EXP0017 adapter-backed reference context packages."""
from __future__ import annotations
from typing import Mapping, Any
from strategy_factory_contracts_v3 import KnownTimeChain, UtcInstant, canonical_sha256
from .enums import *
from .manifest import ContextPackageManifest, SourceRequirement, ComponentReference, ManualPolicyReference, TaskReference
from .lifecycle import ContextObservation
from .feature import FeatureDescriptor, FeatureValue, FeatureFrame
from .representation import RepresentationViewDescriptor
from .cluster import ClusterRule
from .package import ContextPackage

_MODES=AvailabilityMode.RESEARCH|AvailabilityMode.TESTER|AvailabilityMode.PAPER|AvailabilityMode.SHADOW|AvailabilityMode.LIVE

def _t(ms:int)->UtcInstant: return UtcInstant(ms,"fixture.utc")
def _chain(source:Mapping[str,Any])->KnownTimeChain:
    event=int(source["event_time_ms"]); known=int(source.get("known_time_ms",event)); confirmed=int(source.get("confirmation_time_ms",known)); cut=int(source.get("observation_cut_ms",confirmed)); decision=int(source.get("decision_time_ms",cut))
    return KnownTimeChain(_t(event),_t(known),_t(confirmed),_t(cut),_t(decision))

class SyntheticBreakContextPackage(ContextPackage):
    def __init__(self)->None:
        self._features=tuple(sorted((
            FeatureDescriptor("break.direction","1.0.0","alpha_lab",FeatureDataType.CATEGORY,"side",(),MissingnessPolicy.REJECT,StalenessPolicy.REJECT,0,(),_MODES,True,("long","short"),"Direction of the confirmed break."),
            FeatureDescriptor("break.distance_atr","1.0.0","alpha_lab",FeatureDataType.FLOAT64,"atr",(),MissingnessPolicy.REJECT,StalenessPolicy.REJECT,0,(),_MODES,True,(),"Close displacement beyond the prior range normalized by ATR."),
            FeatureDescriptor("break.range_atr","1.0.0","alpha_lab",FeatureDataType.FLOAT64,"atr",(),MissingnessPolicy.REJECT,StalenessPolicy.REJECT,0,(),_MODES,True,(),"Prior range size normalized by ATR."),
            FeatureDescriptor("market.spread_points","1.0.0","alpha_lab",FeatureDataType.FLOAT64,"points",(),MissingnessPolicy.EXPLICIT_MISSING,StalenessPolicy.MARK_STALE,2000,(),_MODES,True,(),"Observed spread at decision cut."),
            FeatureDescriptor("time.session","1.0.0","alpha_lab",FeatureDataType.CATEGORY,"session",(),MissingnessPolicy.REJECT,StalenessPolicy.ALLOW_WITH_AGE,86400000,(),_MODES,True,("asia","london","new_york","off_hours"),"Causal session label."),
        ),key=lambda x:x.feature_id))
        feature_hash=canonical_sha256([x.material() for x in self._features])
        self._views=(
            RepresentationViewDescriptor("break.tabular","1.0.0","alpha_lab",RepresentationKind.TABULAR,tuple(x.feature_id for x in self._features),(5,),_MODES,True,{"ordering":"lexicographic"}),
            RepresentationViewDescriptor("break.sequence","1.0.0","alpha_lab",RepresentationKind.SEQUENCE,("break.distance_atr","market.spread_points"),(2,16),AvailabilityMode.RESEARCH|AvailabilityMode.TESTER,False,{"window":16}),
        )
        self._clusters=(
            ClusterRule("break.opportunity","1.0.0","alpha_lab",ClusterKind.OPPORTUNITY,("symbol","timeframe_seconds","signal_bar_open_ms","direction"),{}),
            ClusterRule("break.session_day","1.0.0","alpha_lab",ClusterKind.SYMBOL_SESSION_DAY,("symbol","trading_day","session"),{}),
        )
        self._manifest=ContextPackageManifest("ucee.reference.synthetic_break","1.0.0","alpha_lab","doctrine.synthetic_break","1.0.0","ucee.reference.break_adapter","1.0.0",ContextUpdateScope.NEW_BAR|ContextUpdateScope.REPLAY|ContextUpdateScope.HISTORY_REBUILD,_MODES,
            (SourceRequirement("primary_m1",SourceRequirementKind.CLOSED_BARS,RequirementStrength.REQUIRED,("PRIMARY",),60,64,120000,"primary_m1","closed-bar causal break detection"),SourceRequirement("primary_spec",SourceRequirementKind.SYMBOL_SPEC,RequirementStrength.REQUIRED,("PRIMARY",),0,1,60000,"none","price and spread normalization")),
            (ComponentReference("break.core_features","1.0.0",feature_hash,True),),tuple(ComponentReference(x.view_id,x.version,x.descriptor_hash,True) for x in self._views),tuple(ComponentReference(x.rule_id,x.version,x.rule_hash,True) for x in self._clusters),
            (ManualPolicyReference("break.manual_close_confirmed","1.0.0",ManualPolicyKind.BASELINE_SETUP,("break.direction","break.distance_atr")),),
            (TaskReference("break.tradeability","1.0.0",TaskKind.BINARY,"label.net_r_positive",("break.tabular","break.sequence")),),description="Synthetic causal reference context used to prove package conformance without strategy doctrine ambiguity.")
    @property
    def manifest(self): return self._manifest
    def feature_descriptors(self): return self._features
    def view_descriptors(self): return self._views
    def cluster_rules(self): return self._clusters
    def observe(self,source):
        required=("symbol","timeframe_seconds","signal_bar_open_ms","event_time_ms","prior_high","prior_low","close","atr")
        if any(k not in source for k in required): return ()
        close=float(source["close"]); hi=float(source["prior_high"]); lo=float(source["prior_low"])
        if close<=hi and close>=lo: return ()
        direction="long" if close>hi else "short"
        payload={"atr":float(source["atr"]),"close":close,"direction":direction,"prior_high":hi,"prior_low":lo,"signal_bar_open_ms":int(source["signal_bar_open_ms"]),"spread_points":source.get("spread_points"),"session":str(source.get("session","off_hours")),"trading_day":str(source.get("trading_day","unknown"))}
        observation=ContextObservation(self.manifest.package_id,self.manifest.version,(str(source.get("source_event_id","synthetic_break_event")),),(str(source["symbol"]),),(int(source["timeframe_seconds"]),),ContextLifecycleState.CONFIRMED,_chain(source),payload)
        return (observation,)
    def build_feature_frame(self,observation,source):
        p=observation.payload; atr=float(p["atr"]); direction=str(p["direction"]); boundary=float(p["prior_high"] if direction=="long" else p["prior_low"]); distance=abs(float(p["close"])-boundary)/atr; range_atr=abs(float(p["prior_high"])-float(p["prior_low"]))/atr
        raw={"break.direction":direction,"break.distance_atr":distance,"break.range_atr":range_atr,"market.spread_points":p.get("spread_points"),"time.session":p["session"]}
        values=[]
        for d in self._features:
            missing=raw[d.feature_id] is None
            values.append(FeatureValue(d.feature_id,d.version,None if missing else raw[d.feature_id],observation.time_chain.observation_cut,observation.time_chain.confirmation_time,missing,"source_missing" if missing else "none"))
        return FeatureFrame(observation.observation_id,self.manifest.package_id,self.manifest.version,observation.time_chain.observation_cut,self._features,tuple(values))

class EXP0017ContextPackage(ContextPackage):
    """Reference package consuming canonical records emitted by the existing SF20 EXP0017 adapter."""
    def __init__(self)->None:
        self._features=tuple(sorted((
            FeatureDescriptor("exp0017.direction","1.0.0","alpha_lab",FeatureDataType.CATEGORY,"side",(),MissingnessPolicy.REJECT,StalenessPolicy.REJECT,0,(),_MODES,True,("long","short"),"Mapped divergence direction."),
            FeatureDescriptor("exp0017.group_minutes","1.0.0","alpha_lab",FeatureDataType.INT64,"minutes",(),MissingnessPolicy.REJECT,StalenessPolicy.ALLOW_WITH_AGE,86400000,(),_MODES,True,(),"Cycle group duration."),
            FeatureDescriptor("exp0017.hunter_displacement","1.0.0","alpha_lab",FeatureDataType.FLOAT64,"price",(),MissingnessPolicy.REJECT,StalenessPolicy.REJECT,0,(),_MODES,True,(),"Hunter displacement from reference."),
            FeatureDescriptor("exp0017.clean_displacement","1.0.0","alpha_lab",FeatureDataType.FLOAT64,"price",(),MissingnessPolicy.REJECT,StalenessPolicy.REJECT,0,(),_MODES,True,(),"Clean-symbol displacement from reference."),
            FeatureDescriptor("exp0017.divergence_gap","1.0.0","alpha_lab",FeatureDataType.FLOAT64,"price",(),MissingnessPolicy.REJECT,StalenessPolicy.REJECT,0,(),_MODES,True,(),"Absolute displacement divergence."),
        ),key=lambda x:x.feature_id))
        self._views=(RepresentationViewDescriptor("exp0017.tabular","1.0.0","alpha_lab",RepresentationKind.TABULAR,tuple(x.feature_id for x in self._features),(5,),_MODES,True,{"ordering":"lexicographic"}),RepresentationViewDescriptor("exp0017.intermarket","1.0.0","alpha_lab",RepresentationKind.INTERMARKET,("exp0017.hunter_displacement","exp0017.clean_displacement"),(2,1),AvailabilityMode.RESEARCH|AvailabilityMode.TESTER,False,{"symbols":2}))
        self._clusters=(ClusterRule("exp0017.opportunity","1.0.0","alpha_lab",ClusterKind.OPPORTUNITY,("trading_day","group_minutes","direction","hunter_symbol","clean_symbol"),{}),ClusterRule("exp0017.parent_cycle","1.0.0","alpha_lab",ClusterKind.PARENT_CHILD,("trading_day","group_minutes","current_cycle_start_ms"),{}))
        self._manifest=ContextPackageManifest("ucee.reference.exp0017","1.0.0","alpha_lab","exp0017.temporal_intermarket_divergence","1.0.0","sf20.exp0017.adapter","1.0.0",ContextUpdateScope.TIMER|ContextUpdateScope.REPLAY|ContextUpdateScope.HISTORY_REBUILD,_MODES,
            (SourceRequirement("sf20_exp0017_event",SourceRequirementKind.ANATOMY_EVENT,RequirementStrength.REQUIRED,("HUNTER","CLEAN"),60,1,120000,"exp0017_pair_m1","canonical SF20 EXP0017 anatomy event"),),
            (ComponentReference("exp0017.core_features","1.0.0",canonical_sha256([x.material() for x in self._features]),True),),tuple(ComponentReference(x.view_id,x.version,x.descriptor_hash,True) for x in self._views),tuple(ComponentReference(x.rule_id,x.version,x.rule_hash,True) for x in self._clusters),
            (ManualPolicyReference("exp0017.manual_divergence_baseline","1.0.0",ManualPolicyKind.BASELINE_SETUP,("exp0017.direction","exp0017.divergence_gap")),),
            (TaskReference("exp0017.tradeability","1.0.0",TaskKind.BINARY,"label.net_r_positive",("exp0017.tabular","exp0017.intermarket")),),description="Reference package wrapping the accepted SF20 EXP0017 adapter output without moving trade decisions into context truth.")
    @property
    def manifest(self): return self._manifest
    def feature_descriptors(self): return self._features
    def view_descriptors(self): return self._views
    def cluster_rules(self): return self._clusters
    def observe(self,source):
        required=("canonical_event_id","event_time_ms","known_time_ms","confirmation_time_ms","hunter_symbol","clean_symbol","group_minutes","direction","hunter_reference_price","clean_reference_price","hunter_current_extreme","clean_current_extreme","trading_day","current_cycle_start_ms")
        if any(k not in source for k in required): return ()
        payload={k:source[k] for k in required if k not in ("canonical_event_id","event_time_ms","known_time_ms","confirmation_time_ms")}
        return (ContextObservation(self.manifest.package_id,self.manifest.version,(str(source["canonical_event_id"]),),(str(source["hunter_symbol"]),str(source["clean_symbol"])),(60,),ContextLifecycleState.CONFIRMED,_chain(source),payload,str(source.get("parent_event_id","none"))),)
    def build_feature_frame(self,observation,source):
        p=observation.payload; hunter=float(p["hunter_current_extreme"])-float(p["hunter_reference_price"]); clean=float(p["clean_current_extreme"])-float(p["clean_reference_price"])
        raw={"exp0017.direction":str(p["direction"]),"exp0017.group_minutes":int(p["group_minutes"]),"exp0017.hunter_displacement":hunter,"exp0017.clean_displacement":clean,"exp0017.divergence_gap":abs(hunter-clean)}
        values=tuple(FeatureValue(d.feature_id,d.version,raw[d.feature_id],observation.time_chain.observation_cut,observation.time_chain.confirmation_time,False,"none") for d in self._features)
        return FeatureFrame(observation.observation_id,self.manifest.package_id,self.manifest.version,observation.time_chain.observation_cut,self._features,values)
