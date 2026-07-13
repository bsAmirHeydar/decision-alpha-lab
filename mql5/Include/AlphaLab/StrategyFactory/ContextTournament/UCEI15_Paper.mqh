#ifndef ALPHALAB_UCEI15_PAPER_MQH
#define ALPHALAB_UCEI15_PAPER_MQH
bool UCEI15_PaperPlanPass(const long start_ms,const long end_ms,const int minimum_decisions,const bool retraining_allowed,const bool tuning_allowed){return(start_ms<end_ms&&minimum_decisions>0&&!retraining_allowed&&!tuning_allowed);}
bool UCEI15_ReconciliationPass(const double expected_entry,const double observed_entry,const double expected_cost,const double observed_cost,const double tolerance){return(MathAbs(expected_entry-observed_entry)<=tolerance&&MathAbs(expected_cost-observed_cost)<=tolerance);}
#endif
