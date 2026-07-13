#ifndef __UCEI09_SURVIVAL_CONTRACTS_MQH__
#define __UCEI09_SURVIVAL_CONTRACTS_MQH__
struct UCEI09_SurvivalCurve{string curve_id;string row_id;long horizons_ms[];double survival[];double cumulative_hazard[];string model_key;string evidence_hash;bool Valid()const{int n=ArraySize(horizons_ms);if(curve_id=="" || n<1 || ArraySize(survival)!=n || ArraySize(cumulative_hazard)!=n)return false;for(int i=0;i<n;i++){if(survival[i]<0.0 || survival[i]>1.0)return false;if(i>0 && survival[i]>survival[i-1])return false;}return true;}};
struct UCEI09_CompetingRiskCurve{string curve_id;string row_id;long horizons_ms[];int cause_ids[];double overall_survival[];string evidence_hash;};
#endif
