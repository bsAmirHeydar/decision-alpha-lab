#ifndef AL_ACL04_TREATMENT_ENVELOPE_MQH
#define AL_ACL04_TREATMENT_ENVELOPE_MQH

struct AL_ACL04_TreatmentEnvelope
  {
   string envelope_id;
   string envelope_digest;
   string context_id;
   string context_version;
   string upstream_handoff_digest;
   double max_risk_units;
   bool   protective_reference_required;
   bool   live_order_submission_allowed;
   bool   capital_activation_allowed;
  };

bool AL_ACL04_TreatmentEnvelopeIsResearchOnly(const AL_ACL04_TreatmentEnvelope &envelope)
  {
   return(envelope.max_risk_units>0.0 &&
          envelope.protective_reference_required &&
          !envelope.live_order_submission_allowed &&
          !envelope.capital_activation_allowed &&
          StringFind(envelope.envelope_digest,"sha256:")==0);
  }

#endif
