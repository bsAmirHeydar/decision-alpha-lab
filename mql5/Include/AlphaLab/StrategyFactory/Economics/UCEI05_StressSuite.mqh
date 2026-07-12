#ifndef UCEI05_STRESS_SUITE_MQH
#define UCEI05_STRESS_SUITE_MQH
#include "UCEI05_ReservationLedger.mqh"
class CUCEI05StressSuite {
public:
 bool NonImprovingVolume(const UCEI05_EconomicEnvelope &baseline,const UCEI05_EconomicEnvelope &stressed) const { return(stressed.volume<=baseline.volume+1e-12); }
 bool RiskWithinBudget(const UCEI05_EconomicEnvelope &e,const double tolerance=1e-8) const { return(!e.accepted || e.maximum_loss_cash<=e.risk_budget_cash+tolerance); }
};
#endif
