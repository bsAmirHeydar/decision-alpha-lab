#ifndef __SF10_CUSTOM_OBJECTIVE_MQH__
#define __SF10_CUSTOM_OBJECTIVE_MQH__
#include "SF10_ResearchMetrics.mqh"

struct SF10_ObjectiveConfig
{
   string schema;
   ENUM_SF10_OBJECTIVE_MODE mode;
   long minimum_unique_events;
   long minimum_filled_outcomes;
   double minimum_fill_rate;
   double minimum_expectancy_r;
   double drawdown_penalty_weight;
   double dispersion_penalty_weight;
   double tail_dependency_penalty_weight;
   double minimum_fold_survival;
   double minimum_cost_survival;
   double minimum_stability;
};

struct SF10_ObjectiveResult
{
   double score;
   ENUM_SF10_PASS_STATUS status;
   string reason;
};

SF10_ObjectiveResult SF10_EvaluateObjective(const SF10_ResearchMetrics &m,const SF10_ObjectiveConfig &c)
{
   SF10_ObjectiveResult r;r.score=-1.0e100;r.status=SF10_PASS_VALID;r.reason="";
   if(!MathIsValidNumber(m.expectancy_r)||!MathIsValidNumber(m.maximum_drawdown_r)||!MathIsValidNumber(m.standard_deviation_r))
   {r.status=SF10_PASS_REJECTED_NONFINITE;r.reason="non-finite research metric";return r;}
   if(m.unique_event_count<c.minimum_unique_events||m.filled_count<c.minimum_filled_outcomes)
   {r.status=SF10_PASS_REJECTED_MIN_SAMPLE;r.reason="minimum sample gate failed";return r;}
   if(m.fill_rate<c.minimum_fill_rate)
   {r.status=SF10_PASS_REJECTED_FILL_RATE;r.reason="minimum fill-rate gate failed";return r;}
   if(m.expectancy_r<c.minimum_expectancy_r)
   {r.status=SF10_PASS_REJECTED_EXPECTANCY;r.reason="minimum expectancy gate failed";return r;}
   if(m.fold_survival_score<c.minimum_fold_survival||m.cost_survival_score<c.minimum_cost_survival||m.stability_score<c.minimum_stability)
   {r.status=SF10_PASS_REJECTED_RECONCILIATION;r.reason="survival or stability gate failed";return r;}
   const double sample_scale=MathSqrt((double)MathMax(1,m.unique_event_count));
   const double survival=m.fold_survival_score*m.cost_survival_score*m.stability_score;
   double penalty=1.0+c.drawdown_penalty_weight*m.maximum_drawdown_r+
                  c.dispersion_penalty_weight*m.standard_deviation_r+
                  c.tail_dependency_penalty_weight*MathMax(0.0,m.best_trade_share);
   if(c.mode==SF10_OBJECTIVE_EXPECTANCY)penalty=1.0;
   else if(c.mode==SF10_OBJECTIVE_STABILITY_WEIGHTED)penalty=1.0+c.drawdown_penalty_weight*m.maximum_drawdown_r;
   else if(c.mode==SF10_OBJECTIVE_TAIL_AWARE)penalty=1.0+c.drawdown_penalty_weight*m.maximum_drawdown_r+c.tail_dependency_penalty_weight*MathMax(0.0,m.best_trade_share);
   r.score=(m.expectancy_r*sample_scale*survival)/MathMax(0.0000001,penalty);
   r.status=SF10_PASS_VALID;r.reason="accepted";return r;
}
#endif
