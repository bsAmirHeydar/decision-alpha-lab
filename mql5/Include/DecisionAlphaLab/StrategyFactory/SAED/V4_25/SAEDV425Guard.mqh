#ifndef __SAED_V4_25_GUARD_MQH__
#define __SAED_V4_25_GUARD_MQH__
#include "SAEDV425Types.mqh"
ENUM_SAEDV425_PATH SAEDV425GuardPath(const bool has_source,const ENUM_SAEDV425_DRIFT_CLASS drift_class,const double support,const double ood_pvalue,const double conformal_lower_bound,const bool retrospective_negative_transfer){ if(!has_source) return SAEDV425_SCRATCH_BASELINE; if(drift_class==SAEDV425_NOVEL) return SAEDV425_SCRATCH_BASELINE; if(support<0.5 || ood_pvalue<0.05 || conformal_lower_bound<-0.1) return SAEDV425_SCRATCH_BASELINE; if(retrospective_negative_transfer) return SAEDV425_SCRATCH_BASELINE; return SAEDV425_TRANSFER_CANDIDATE; }
#endif
