#ifndef SAEDV415_VIEW_MASK_MQH
#define SAEDV415_VIEW_MASK_MQH
// SAED_V4_15 explicit missingness; zero is never interpreted as present without the mask.
bool SAEDV415IsAvailable(const bool available,const double quality,const int age_seconds,const double min_quality,const int max_age){ return available && quality>=min_quality && age_seconds<=max_age; }
#endif
