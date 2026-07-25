from __future__ import annotations
from decimal import Decimal as D
from .contracts import *
from .enums import *
from .splits import build_purged_embargoed_plan

def golden_anchors(count:int=6):
    out=[]
    for i in range(count):
        t=1_700_000_000_000+i*3_600_000
        src=SourceRef("market.EURUSD","r1",f"src{i:02d}",t)
        out.append(OpportunityAnchor("context.synthetic@1.0.0",f"ctx.{i:02d}",f"cluster.{i//2:02d}","EURUSD","M5",TradeSide.LONG if i%2==0 else TradeSide.SHORT,t,t,t,f"frame{i:02d}",{"tabular":f"view{i:02d}"},(src,),True,"",{"regime":"reference"}))
    return tuple(out)

def golden_path(anchor:OpportunityAnchor):
    base=D("1.1000")
    if anchor.side==TradeSide.LONG:
        mids=[base,base+D("0.0003"),base+D("0.0007"),base+D("0.0012"),base+D("0.0018"),base+D("0.0013")]
    else:
        mids=[base,base-D("0.0003"),base-D("0.0007"),base-D("0.0012"),base-D("0.0018"),base-D("0.0013")]
    return tuple(PathObservation(i,anchor.decision_time_ms+i*60_000,anchor.decision_time_ms+i*60_000,m-D("0.00005"),m+D("0.00005"),D("2"),"r1",False) for i,m in enumerate(mids))

def golden_treatments(anchor:OpportunityAnchor):
    long=anchor.side==TradeSide.LONG; entry=D("1.10005") if long else D("1.09995")
    stop=entry-D("0.0005") if long else entry+D("0.0005")
    target=entry+D("0.0010") if long else entry-D("0.0010")
    env="econ.reference"
    return (
      TreatmentSibling(f"t.{anchor.context_occurrence_id}.tight","family.tight",anchor.side,EntryStyle.MARKET,None,stop,target,None,0,300_000,D("1"),D("100000"),D("2"),D("55"),env,True,"",True,{"style":"tight_fixed"}),
      TreatmentSibling(f"t.{anchor.context_occurrence_id}.runner","family.runner",anchor.side,EntryStyle.MARKET,None,stop,None,D("0.0004"),0,300_000,D("1"),D("100000"),D("2"),D("55"),env,True,"",False,{"style":"runner"}),
    )

def golden_scenarios():
    return (EconomicScenario("economics.baseline","1.0.0",D("2"),D("0"),D("0"),D("0"),D("1")),EconomicScenario("economics.stressed","1.0.0",D("4"),D("0.00002"),D("1"),D("1"),D("1.25")))

def golden_tasks():
    return (
      LabelTaskContract("task.trade.net_r_positive","1.0.0",TaskKind.BINARY,"net_r",300_000,"economics.baseline@1.0.0",D("0"),UtilityDirection.MAXIMIZE,(LabelMaturityPolicy.REQUIRE_RESOLVED,),"opportunity"),
      LabelTaskContract("task.treatment.rank","1.0.0",TaskKind.RANKING,"net_r",300_000,"economics.baseline@1.0.0",D("0"),UtilityDirection.MAXIMIZE,(LabelMaturityPolicy.REQUIRE_RESOLVED,LabelMaturityPolicy.REQUIRE_ALL_SIBLINGS),"opportunity"),
      LabelTaskContract("task.choice.best","1.0.0",TaskKind.TREATMENT_CHOICE,"net_r",300_000,"economics.baseline@1.0.0",D("0"),UtilityDirection.MAXIMIZE,(LabelMaturityPolicy.REQUIRE_RESOLVED,LabelMaturityPolicy.REQUIRE_ALL_SIBLINGS),"opportunity"),
    )
