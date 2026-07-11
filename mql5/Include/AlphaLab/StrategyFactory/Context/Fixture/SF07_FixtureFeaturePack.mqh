#ifndef __SF07_FIXTURE_FEATURE_PACK_MQH__
#define __SF07_FIXTURE_FEATURE_PACK_MQH__
#include "SF07_EventDirectionNode.mqh"
#include "SF07_RiskDistanceNode.mqh"
#include "SF07_ReferenceMagnitudeNode.mqh"
#include "SF07_NormalizedRiskNode.mqh"
#include "SF07_ConvictionSeedNode.mqh"
class CSF07FixtureFeaturePack
{
private:
   CSF07EventDirectionNode m_direction;
   CSF07RiskDistanceNode m_risk;
   CSF07ReferenceMagnitudeNode m_reference;
   CSF07NormalizedRiskNode m_normalized;
   CSF07ConvictionSeedNode m_conviction;
public:
   bool RegisterAll(CSF07FeatureRegistry &registry,string &error)
   {
      if(!registry.RegisterNode(&m_direction,error))return false;
      if(!registry.RegisterNode(&m_risk,error))return false;
      if(!registry.RegisterNode(&m_reference,error))return false;
      if(!registry.RegisterNode(&m_normalized,error))return false;
      if(!registry.RegisterNode(&m_conviction,error))return false;
      return true;
   }
   bool BuildDefaultVectorSchema(CSF07FeatureVectorSchema &schema,string &error)
   {
      schema.schema_id="sf07.reference_context_vector";schema.schema_version="1.0.0";
      if(!schema.Add("event_direction",SF01_FEATURE_INTEGER,SF07_MISSING_FAIL,0.0,error))return false;
      if(!schema.Add("risk_distance",SF01_FEATURE_DOUBLE,SF07_MISSING_FAIL,0.0,error))return false;
      if(!schema.Add("normalized_risk",SF01_FEATURE_DOUBLE,SF07_MISSING_FAIL,0.0,error))return false;
      if(!schema.Add("conviction_seed",SF01_FEATURE_DOUBLE,SF07_MISSING_FAIL,0.0,error))return false;
      return true;
   }
};
#endif
