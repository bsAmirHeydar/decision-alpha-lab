#ifndef SAED_V4_27_BUDGET_MQH
#define SAED_V4_27_BUDGET_MQH
bool SAEDV427WithinBudget(const int observed,const int limit){ return observed>=0 && observed<=limit; }
#endif
