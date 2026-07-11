#ifndef __SF04_PLUGIN_SELECTION_MQH__
#define __SF04_PLUGIN_SELECTION_MQH__
#include "SF04_PluginDescriptor.mqh"
struct SF04_PluginSelection{string plugin_id;string exact_version;ulong required_capabilities;string expected_descriptor_hash;};
bool SF04_ValidatePluginSelection(const SF04_PluginSelection &v,string &e){if(!SF01_IsSafeIdentifier(v.plugin_id,128)){e="invalid selected plugin";return false;}if(!SF04_IsSemanticVersion(v.exact_version)){e="exact version required";return false;}if(v.expected_descriptor_hash!=""&&!SF01_IsSafeIdentifier(v.expected_descriptor_hash,128)){e="invalid descriptor hash";return false;}e="";return true;}
bool SF04_DescriptorMatchesSelection(const SF04_PluginDescriptor &d,const SF04_PluginSelection &s,string &e){if(d.plugin_id!=s.plugin_id){e="plugin id mismatch";return false;}if(d.version!=s.exact_version){e="version mismatch";return false;}if(!SF04_HasCapability(d.capability_mask,s.required_capabilities)){e="capability mismatch";return false;}if(s.expected_descriptor_hash!=""&&SF04_PluginDescriptorHash(d)!=s.expected_descriptor_hash){e="descriptor hash mismatch";return false;}e="";return true;}
#endif
