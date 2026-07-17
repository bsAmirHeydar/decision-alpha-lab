#ifndef DAL_SAED_V426_FAITHFULNESS_MQH
#define DAL_SAED_V426_FAITHFULNESS_MQH
bool SAEDV426FaithfulnessGate(const double correlation,const double floor,const double deletion_drop,const double drop_floor){ return correlation>=floor && deletion_drop>=drop_floor; }
#endif
