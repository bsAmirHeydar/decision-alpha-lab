from dataclasses import dataclass
from .models import ResearchMetrics
from .enums import DifferentialStatus
@dataclass(frozen=True,slots=True)
class DifferentialTolerance: net_r_absolute:float=.01; fill_rate_absolute:float=.01; drawdown_absolute:float=.01; count_absolute:int=0
@dataclass(frozen=True,slots=True)
class DifferentialResult: status:DifferentialStatus; net_r_delta:float; fill_rate_delta:float; drawdown_delta:float; count_delta:int; reason:str

def compare_metrics(a:ResearchMetrics,b:ResearchMetrics,t:DifferentialTolerance=DifferentialTolerance())->DifferentialResult:
    dr=b.total_net_r-a.total_net_r; df=b.fill_rate-a.fill_rate; dd=b.maximum_drawdown_r-a.maximum_drawdown_r; dc=b.filled_count-a.filled_count
    exact=abs(dr)<1e-12 and abs(df)<1e-12 and abs(dd)<1e-12 and dc==0
    within=abs(dr)<=t.net_r_absolute and abs(df)<=t.fill_rate_absolute and abs(dd)<=t.drawdown_absolute and abs(dc)<=t.count_absolute
    return DifferentialResult(DifferentialStatus.MATCH if exact else DifferentialStatus.WITHIN_TOLERANCE if within else DifferentialStatus.MISMATCH,dr,df,dd,dc,"exact match" if exact else "within configured tolerance" if within else "divergence exceeds tolerance")
