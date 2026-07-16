#property strict
#ifndef SAEDV423BUDGET_MQH
#define SAEDV423BUDGET_MQH
// SAED_V4_23 static mirror. Research-only; no broker, runtime, promotion or execution authority.
struct SAEDV423Budget { int trials; int candidates; int evaluations; int hidden_queries; };
bool SAEDV423BudgetSafe(const SAEDV423Budget &b){ return b.hidden_queries==0; }

#endif
