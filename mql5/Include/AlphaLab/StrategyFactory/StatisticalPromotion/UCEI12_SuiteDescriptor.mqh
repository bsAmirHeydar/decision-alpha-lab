#ifndef __UCEI12_SUITE_DESCRIPTOR_MQH__
#define __UCEI12_SUITE_DESCRIPTOR_MQH__

struct UCEI12_SuiteDescriptor
  {
   string key;
   string version;
   bool   critical;
   bool   deterministic;
   bool   seed_required;
   string required_inputs;
   string outputs;

   string RegistryKey() const { return key+"@"+version; }
   bool Valid() const { return key!="" && version!="" && required_inputs!="" && outputs!=""; }
  };

#endif
