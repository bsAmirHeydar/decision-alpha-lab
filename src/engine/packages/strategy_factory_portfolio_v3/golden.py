from __future__ import annotations
from .contracts import *
from .enums import *
H='a'*64

def evidence(context):
    return PromotionEvidence(context,H,PromotionStatus.PROMOTE,H,True),CalibrationEvidence(context,'1.0.0',H,GateStatus.PASS,0.05,500)
def candidate(i,context,symbol,side,utility=1.0,risk=1.0,currency='USD',cluster='macro'):
    p,c=evidence(context)
    return OpportunityCandidate(f'cand-{i}',f'occ-{i}',context,'1.0.0',1000,100000,symbol,currency,'new-york','hook',cluster,side,utility,0.1,0.5,0.9,utility,0.5,risk,5.0,0.01,p,c,H,H)
def golden_batch():
    return OpportunityBatch('batch-golden','1.0.0',2000,(candidate(1,'ctx-a','EURUSD',Side.LONG,1.2),candidate(2,'ctx-b','XAUUSD',Side.SHORT,1.0),candidate(3,'ctx-c','NAS100',Side.LONG,0.8)) ,(H,))
def golden_model(): return DependenceModel('dep-golden','1.0.0',2000,(),0.85,1.0,0.8,0.6,0.7,0.75)
def golden_limits(): return PortfolioLimits('limits-golden','1.0.0',4,2,3,2,3,4,4,3,10,0.2,1.0,2)
def golden_stress(): return (StressScenario('drop-ctx-a',0.0,0.2,1.5,'ctx-a',0.1),StressScenario('corr-shock',1.0,0.3,2.0,None,0.2))
