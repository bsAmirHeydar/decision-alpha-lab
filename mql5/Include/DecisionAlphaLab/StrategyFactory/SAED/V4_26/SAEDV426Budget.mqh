#ifndef DAL_SAED_V426_BUDGET_MQH
#define DAL_SAED_V426_BUDGET_MQH
bool SAEDV426WithinBudget(const long used,const long maximum){ return used>=0 && used<=maximum; }
#endif
