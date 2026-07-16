#ifndef SAEDV415_MISSINGNESS_GUARD_MQH
#define SAEDV415_MISSINGNESS_GUARD_MQH
// SAED_V4_15 missing foundation plane falls back to baseline.
int SAEDV415FoundationDirective(const int foundation_count,const bool required){ if(required && foundation_count<1)return 1; return 0; }
#endif
