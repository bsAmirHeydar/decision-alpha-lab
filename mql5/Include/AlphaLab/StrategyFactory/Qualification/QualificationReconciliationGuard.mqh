#ifndef ALPHALAB_QUALIFICATION_RECONCILIATION_GUARD_MQH
#define ALPHALAB_QUALIFICATION_RECONCILIATION_GUARD_MQH
bool ALQualificationReconciles(const string reserved_hash,const string observed_hash,const int expected_count,const int observed_count,const double expected_risk,const double observed_risk){
   if(reserved_hash!=observed_hash) return false; // reserved_hash!=observed_hash
   if(expected_count!=observed_count) return false;
   if(MathAbs(expected_risk-observed_risk)>1e-9) return false;
   return true;
}
#endif
