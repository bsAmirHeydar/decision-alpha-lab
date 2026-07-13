#ifndef ALPHALAB_PORTFOLIO_RECONCILIATION_MQH
#define ALPHALAB_PORTFOLIO_RECONCILIATION_MQH
bool ALReservationReconciles(const int expected_count,const int observed_count,const double expected_risk,const double observed_risk){ return expected_count==observed_count && MathAbs(expected_risk-observed_risk)<=1e-9; }
#endif
