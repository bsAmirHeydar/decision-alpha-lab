#ifndef AL_ACL04_HANDOFF_BINDING_MQH
#define AL_ACL04_HANDOFF_BINDING_MQH

struct AL_ACL04_UpstreamBinding
  {
   string handoff_type;
   string context_id;
   string context_version;
   string upstream_handoff_digest;
   string upstream_manifest_digest;
   string source_snapshot_digest;
   bool   known_time_guards_required;
   bool   search_authority_required;
  };

bool AL_ACL04_UpstreamBindingIsComplete(const AL_ACL04_UpstreamBinding &binding)
  {
   return(binding.handoff_type=="ACL03_TO_ACL04" &&
          StringLen(binding.context_id)>0 &&
          StringLen(binding.context_version)>0 &&
          StringFind(binding.upstream_handoff_digest,"sha256:")==0 &&
          StringFind(binding.upstream_manifest_digest,"sha256:")==0 &&
          binding.known_time_guards_required &&
          binding.search_authority_required);
  }

#endif
