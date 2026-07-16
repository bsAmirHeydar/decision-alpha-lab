#ifndef SAEDV422_BUDGET_MQH
#define SAEDV422_BUDGET_MQH
bool SAEDV422BudgetAvailable(const int used,const int requested,const int limit){return used>=0&&requested>=0&&used+requested<=limit;}
#endif
