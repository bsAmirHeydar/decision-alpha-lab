#ifndef __SF07_FEATURE_DESCRIPTOR_MQH__
#define __SF07_FEATURE_DESCRIPTOR_MQH__

#include "../Contracts/SF01_AllContracts.mqh"
#include "SF07_ContextEnums.mqh"

#define SF07_MAX_FEATURE_DEPENDENCIES 16

struct SF07_FeatureDescriptor
{
   string feature_id;
   string feature_version;
   string owner_id;
   ENUM_SF01_FEATURE_TYPE value_type;
   ENUM_SF07_UPDATE_SCOPE update_scope;
   bool required;
   bool numeric;
   long max_age_milliseconds;
   int dependency_count;
   string dependencies[SF07_MAX_FEATURE_DEPENDENCIES];
};

void SF07_ResetFeatureDescriptor(SF07_FeatureDescriptor &descriptor)
{
   descriptor.feature_id = "";
   descriptor.feature_version = "";
   descriptor.owner_id = "";
   descriptor.value_type = SF01_FEATURE_NULL;
   descriptor.update_scope = SF07_UPDATE_EVENT;
   descriptor.required = true;
   descriptor.numeric = false;
   descriptor.max_age_milliseconds = 0;
   descriptor.dependency_count = 0;
   for(int i = 0; i < SF07_MAX_FEATURE_DEPENDENCIES; i++) descriptor.dependencies[i] = "";
}

bool SF07_AddDependency(SF07_FeatureDescriptor &descriptor,
                        const string dependency_id,
                        string &error)
{
   if(!SF01_IsSafeIdentifier(dependency_id, 128))
   { error = "invalid dependency id"; return false; }
   if(descriptor.dependency_count >= SF07_MAX_FEATURE_DEPENDENCIES)
   { error = "feature dependency capacity exceeded"; return false; }
   for(int i = 0; i < descriptor.dependency_count; i++)
   {
      if(descriptor.dependencies[i] == dependency_id)
      { error = "duplicate dependency id"; return false; }
   }
   descriptor.dependencies[descriptor.dependency_count] = dependency_id;
   descriptor.dependency_count++;
   error = "";
   return true;
}

bool SF07_ValidateFeatureDescriptor(const SF07_FeatureDescriptor &descriptor,
                                    string &error)
{
   if(!SF01_IsSafeIdentifier(descriptor.feature_id, 128))
   { error = "invalid feature id"; return false; }
   if(!SF01_IsSafeIdentifier(descriptor.feature_version, 64))
   { error = "invalid feature version"; return false; }
   if(!SF01_IsSafeIdentifier(descriptor.owner_id, 128))
   { error = "invalid feature owner"; return false; }
   if(descriptor.value_type == SF01_FEATURE_NULL)
   { error = "feature descriptor cannot use NULL type"; return false; }
   if(descriptor.max_age_milliseconds < 0)
   { error = "negative feature max age"; return false; }
   if(descriptor.dependency_count < 0 || descriptor.dependency_count > SF07_MAX_FEATURE_DEPENDENCIES)
   { error = "invalid dependency count"; return false; }
   for(int i = 0; i < descriptor.dependency_count; i++)
   {
      if(!SF01_IsSafeIdentifier(descriptor.dependencies[i], 128))
      { error = "invalid dependency id"; return false; }
      if(descriptor.dependencies[i] == descriptor.feature_id)
      { error = "feature cannot depend on itself"; return false; }
      for(int j = i + 1; j < descriptor.dependency_count; j++)
      {
         if(descriptor.dependencies[i] == descriptor.dependencies[j])
         { error = "duplicate feature dependency"; return false; }
      }
   }
   error = "";
   return true;
}

string SF07_FeatureDescriptorCanonical(const SF07_FeatureDescriptor &descriptor)
{
   string payload = descriptor.feature_id + "|" + descriptor.feature_version + "|" +
                    descriptor.owner_id + "|" + IntegerToString((int)descriptor.value_type) + "|" +
                    IntegerToString((int)descriptor.update_scope) + "|" +
                    SF01_CanonicalBool(descriptor.required) + "|" +
                    SF01_CanonicalBool(descriptor.numeric) + "|" +
                    IntegerToString(descriptor.max_age_milliseconds);
   for(int i = 0; i < descriptor.dependency_count; i++)
      payload += "|" + descriptor.dependencies[i];
   return payload;
}

string SF07_FeatureDescriptorHash(const SF07_FeatureDescriptor &descriptor)
{
   return SF01_StableId("fdsc", SF07_FeatureDescriptorCanonical(descriptor));
}

#endif
