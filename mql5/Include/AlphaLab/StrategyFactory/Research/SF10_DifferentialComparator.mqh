#ifndef __SF10_DIFFERENTIAL_COMPARATOR_MQH__
#define __SF10_DIFFERENTIAL_COMPARATOR_MQH__
#include "SF10_SelectedPassCollector.mqh"

struct SF10_DifferentialTolerance
{
   double net_r_absolute;
   double fill_rate_absolute;
   double drawdown_absolute;
   long count_absolute;
};
struct SF10_DifferentialResult
{
   ENUM_SF10_DIFFERENTIAL_STATUS status;
   double net_r_delta;
   double fill_rate_delta;
   double drawdown_delta;
   long count_delta;
   string reason;
};

SF10_DifferentialResult SF10_CompareResearchMetrics(const SF10_ResearchMetrics &virtual_metrics,
                                                    const SF10_ResearchMetrics &tester_metrics,
                                                    const SF10_DifferentialTolerance &t)
{
   SF10_DifferentialResult r;r.net_r_delta=tester_metrics.total_net_r-virtual_metrics.total_net_r;
   r.fill_rate_delta=tester_metrics.fill_rate-virtual_metrics.fill_rate;
   r.drawdown_delta=tester_metrics.maximum_drawdown_r-virtual_metrics.maximum_drawdown_r;
   r.count_delta=tester_metrics.filled_count-virtual_metrics.filled_count;
   const bool exact=MathAbs(r.net_r_delta)<0.0000001&&MathAbs(r.fill_rate_delta)<0.0000001&&MathAbs(r.drawdown_delta)<0.0000001&&r.count_delta==0;
   const bool within=MathAbs(r.net_r_delta)<=t.net_r_absolute&&MathAbs(r.fill_rate_delta)<=t.fill_rate_absolute&&
                     MathAbs(r.drawdown_delta)<=t.drawdown_absolute&&MathAbs((double)r.count_delta)<=t.count_absolute;
   if(exact){r.status=SF10_DIFF_MATCH;r.reason="exact match";}
   else if(within){r.status=SF10_DIFF_WITHIN_TOLERANCE;r.reason="within configured tolerance";}
   else {r.status=SF10_DIFF_MISMATCH;r.reason="research/tester divergence exceeds tolerance";}
   return r;
}
#endif
