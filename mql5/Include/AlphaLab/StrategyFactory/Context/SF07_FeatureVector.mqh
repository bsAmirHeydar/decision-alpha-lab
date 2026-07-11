#ifndef __SF07_FEATURE_VECTOR_MQH__
#define __SF07_FEATURE_VECTOR_MQH__

#include "SF07_FeatureRegistry.mqh"

#define SF07_MAX_VECTOR_FEATURES 128

struct SF07_VectorField
{
   string feature_id;
   ENUM_SF01_FEATURE_TYPE expected_type;
   ENUM_SF07_MISSING_POLICY missing_policy;
   double default_value;
};

class CSF07FeatureVectorSchema
{
private:
   SF07_VectorField m_fields[];
public:
   string schema_id;
   string schema_version;

   CSF07FeatureVectorSchema(void)
   {
      ArrayResize(m_fields, 0);
      schema_id = "";
      schema_version = "";
   }

   int Count(void) const { return ArraySize(m_fields); }

   bool Add(const string feature_id,
            const ENUM_SF01_FEATURE_TYPE expected_type,
            const ENUM_SF07_MISSING_POLICY missing_policy,
            const double default_value,
            string &error)
   {
      if(ArraySize(m_fields) >= SF07_MAX_VECTOR_FEATURES)
      { error = "feature vector capacity exceeded"; return false; }
      if(!SF01_IsSafeIdentifier(feature_id, 128))
      { error = "invalid vector feature id"; return false; }
      if(expected_type != SF01_FEATURE_DOUBLE && expected_type != SF01_FEATURE_INTEGER &&
         expected_type != SF01_FEATURE_BOOLEAN && expected_type != SF01_FEATURE_TIMESTAMP)
      { error = "feature vector requires numeric-compatible type"; return false; }
      if(!MathIsValidNumber(default_value))
      { error = "invalid vector default"; return false; }
      const int count = ArraySize(m_fields);
      for(int i = 0; i < count; i++)
         if(m_fields[i].feature_id == feature_id)
         { error = "duplicate vector feature"; return false; }
      ArrayResize(m_fields, count + 1);
      m_fields[count].feature_id = feature_id;
      m_fields[count].expected_type = expected_type;
      m_fields[count].missing_policy = missing_policy;
      m_fields[count].default_value = default_value;
      error = "";
      return true;
   }

   bool At(const int index, SF07_VectorField &field) const
   {
      if(index < 0 || index >= ArraySize(m_fields)) return false;
      field = m_fields[index];
      return true;
   }

   string Canonical(void) const
   {
      string payload = schema_id + "|" + schema_version;
      const int count = ArraySize(m_fields);
      for(int i = 0; i < count; i++)
         payload += "|" + m_fields[i].feature_id + "|" +
                    IntegerToString((int)m_fields[i].expected_type) + "|" +
                    IntegerToString((int)m_fields[i].missing_policy) + "|" +
                    SF01_CanonicalDouble(m_fields[i].default_value);
      return payload;
   }

   string Hash(void) const { return SF01_StableId("vsch", Canonical()); }

   bool ValidateAgainst(const CSF07FeatureRegistry &registry, string &error) const
   {
      if(!SF01_IsSafeIdentifier(schema_id, 128) || !SF01_IsSafeIdentifier(schema_version, 64))
      { error = "invalid vector schema identity"; return false; }
      if(ArraySize(m_fields) <= 0)
      { error = "feature vector schema is empty"; return false; }
      for(int i = 0; i < ArraySize(m_fields); i++)
      {
         SF07_FeatureDescriptor descriptor;
         if(!registry.GetDescriptor(m_fields[i].feature_id, descriptor))
         { error = "vector feature not registered: " + m_fields[i].feature_id; return false; }
         if(descriptor.value_type != m_fields[i].expected_type)
         { error = "vector feature type mismatch: " + m_fields[i].feature_id; return false; }
      }
      error = "";
      return true;
   }
};

class CSF07FixedFeatureVector
{
private:
   double m_values[];
   ENUM_SF01_FEATURE_QUALITY m_quality[];
   string m_feature_ids[];
public:
   string vector_id;
   string event_id;
   string schema_hash;
   long state_generation;

   CSF07FixedFeatureVector(void)
   {
      ArrayResize(m_values, 0);
      ArrayResize(m_quality, 0);
      ArrayResize(m_feature_ids, 0);
      vector_id = "";
      event_id = "";
      schema_hash = "";
      state_generation = 0;
   }

   int Size(void) const { return ArraySize(m_values); }
   bool At(const int index, double &value, ENUM_SF01_FEATURE_QUALITY &quality, string &feature_id) const
   {
      if(index < 0 || index >= ArraySize(m_values)) return false;
      value = m_values[index];
      quality = m_quality[index];
      feature_id = m_feature_ids[index];
      return true;
   }

   bool Build(const CSF07FeatureVectorSchema &schema,
              const CSF01FeatureSnapshot &snapshot,
              string &error)
   {
      const int count = schema.Count();
      ArrayResize(m_values, count);
      ArrayResize(m_quality, count);
      ArrayResize(m_feature_ids, count);
      schema_hash = schema.Hash();
      event_id = snapshot.event_id;
      state_generation = snapshot.state_generation;
      string canonical = event_id + "|" + schema_hash + "|" + IntegerToString(state_generation);
      for(int i = 0; i < count; i++)
      {
         SF07_VectorField field;
         schema.At(i, field);
         m_feature_ids[i] = field.feature_id;
         SF01_FeatureValue feature;
         bool found = snapshot.Get(field.feature_id, feature);
         double numeric_value = field.default_value;
         ENUM_SF01_FEATURE_QUALITY quality = SF01_QUALITY_MISSING;
         if(found)
         {
            quality = feature.quality;
            if(feature.value_type != field.expected_type)
            { error = "vector runtime type mismatch: " + field.feature_id; return false; }
            if(feature.quality == SF01_QUALITY_VALID || feature.quality == SF01_QUALITY_ESTIMATED)
            {
               if(feature.value_type == SF01_FEATURE_DOUBLE) numeric_value = feature.double_value;
               else if(feature.value_type == SF01_FEATURE_INTEGER) numeric_value = (double)feature.integer_value;
               else if(feature.value_type == SF01_FEATURE_BOOLEAN) numeric_value = feature.boolean_value ? 1.0 : 0.0;
               else if(feature.value_type == SF01_FEATURE_TIMESTAMP) numeric_value = (double)feature.timestamp_value.utc_epoch_milliseconds;
            }
            else if(field.missing_policy == SF07_MISSING_FAIL)
            { error = "required vector feature not valid: " + field.feature_id; return false; }
            else if(field.missing_policy == SF07_MISSING_ZERO) numeric_value = 0.0;
         }
         else
         {
            if(field.missing_policy == SF07_MISSING_FAIL)
            { error = "required vector feature missing: " + field.feature_id; return false; }
            if(field.missing_policy == SF07_MISSING_ZERO) numeric_value = 0.0;
         }
         if(!MathIsValidNumber(numeric_value))
         { error = "non-finite vector value"; return false; }
         m_values[i] = numeric_value;
         m_quality[i] = quality;
         canonical += "|" + field.feature_id + "|" + SF01_CanonicalDouble(numeric_value) + "|" + IntegerToString((int)quality);
      }
      vector_id = SF01_StableId("fvec", canonical);
      error = "";
      return true;
   }
};

#endif
