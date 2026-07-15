#ifndef __DECISION_ALPHA_LAB_SAED_V4_11_AUTHORITY_MQH__
#define __DECISION_ALPHA_LAB_SAED_V4_11_AUTHORITY_MQH__
struct SAEDV411AuthorityBoundary
{
   bool read_frozen_v4_10_handoff;
   bool read_frozen_encoder;
   bool train_reference_synthetic_encoder;
   bool predict_outcomes;
   bool rank_treatments;
   bool select_treatment;
   bool allocate_risk;
   bool activate_runtime;
   bool send_order;
};
SAEDV411AuthorityBoundary SAEDV411ReferenceAuthority()
{
   SAEDV411AuthorityBoundary value;
   value.read_frozen_v4_10_handoff=true;
   value.read_frozen_encoder=true;
   value.train_reference_synthetic_encoder=false; // Python research path only.
   value.predict_outcomes=false;
   value.rank_treatments=false;
   value.select_treatment=false;
   value.allocate_risk=false;
   value.activate_runtime=false;
   value.send_order=false;
   return value;
}
#endif
