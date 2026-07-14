#ifndef __FP_I13_OBJECT_BUDGET_MQH__
#define __FP_I13_OBJECT_BUDGET_MQH__
class FP_I13_ObjectBudget { public: static int AllowedOperations(const int requested,const int limit){if(requested<=0)return 0;return requested<limit?requested:limit;}static bool MustDegrade(const int objects,const int limit){return objects>limit;} };
#endif
