from __future__ import annotations
import math
from typing import Iterable

def binomial_upper_tail(successes:int,trials:int,p0:float=0.5)->float|None:
    if trials<=0: return None
    return min(1.0,sum(math.comb(trials,k)*(p0**k)*((1-p0)**(trials-k)) for k in range(successes,trials+1)))
def wilson_lower(successes:int,trials:int,z:float=1.959963984540054)->float|None:
    if trials<=0: return None
    phat=successes/trials; den=1+z*z/trials
    centre=phat+z*z/(2*trials)
    adj=z*math.sqrt((phat*(1-phat)+z*z/(4*trials))/trials)
    return max(0.0,(centre-adj)/den)
def benjamini_hochberg(pvalues:list[tuple[str,float|None]])->dict[str,float|None]:
    valid=sorted([(k,float(p)) for k,p in pvalues if p is not None],key=lambda x:(x[1],x[0]))
    m=len(valid); out={k:None for k,_ in pvalues}; running=1.0
    for rank in range(m,0,-1):
        k,p=valid[rank-1]; running=min(running,p*m/rank); out[k]=min(1.0,running)
    return out
def mean(values:Iterable[float])->float|None:
    xs=list(values); return None if not xs else sum(xs)/len(xs)
def population_std(values:Iterable[float])->float|None:
    xs=list(values)
    if not xs: return None
    mu=sum(xs)/len(xs); return math.sqrt(sum((x-mu)**2 for x in xs)/len(xs))
def max_drawdown(increments:Iterable[float])->float|None:
    xs=list(increments)
    if not xs: return None
    equity=peak=0.0; worst=0.0
    for x in xs:
        equity+=x; peak=max(peak,equity); worst=min(worst,equity-peak)
    return worst
