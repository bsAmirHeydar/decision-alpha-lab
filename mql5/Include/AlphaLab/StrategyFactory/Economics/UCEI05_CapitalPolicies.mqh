#ifndef UCEI05_CAPITAL_POLICIES_MQH
#define UCEI05_CAPITAL_POLICIES_MQH
#include "UCEI05_CostModel.mqh"
class CUCEI05CapitalPolicies {
public:
 UCEI05_CapitalBudget FixedCash(const double cash) const { UCEI05_CapitalBudget b; b.requested_cash=MathMax(0.0,cash); b.approved_cash=b.requested_cash; b.accepted=(b.approved_cash>0.0); b.reason_code=b.accepted?"ok":"zero_budget"; b.budget_id="capital.fixed_cash@1.0.0"; return b; }
 UCEI05_CapitalBudget EquityFraction(const UCEI05_AccountSnapshot &a,const double fraction) const { return FixedCash(a.equity*MathMax(0.0,fraction)); }
 double DrawdownScale(const UCEI05_AccountSnapshot &a,const double start,const double stop) const { if(a.peak_equity<=0.0) return 0.0; double dd=MathMax(0.0,(a.peak_equity-a.equity)/a.peak_equity); if(dd<=start)return 1.0;if(dd>=stop)return 0.0;return (stop-dd)/(stop-start); }
 double CappedKelly(const double pwin,const double payoff,const double fraction,const double cap) const { if(payoff<=0.0)return 0.0; double k=MathMax(0.0,pwin-(1.0-pwin)/payoff); return MathMin(k*MathMax(0.0,fraction),MathMax(0.0,cap)); }
};
#endif
