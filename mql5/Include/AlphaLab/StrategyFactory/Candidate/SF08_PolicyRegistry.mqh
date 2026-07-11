#ifndef __SF08_POLICY_REGISTRY_MQH__
#define __SF08_POLICY_REGISTRY_MQH__
#include "ISF08_EntryPolicy.mqh"
#include "ISF08_StopPolicy.mqh"
#include "ISF08_ExitPolicy.mqh"

class CSF08PolicyRegistry
{
private:
   ISF08EntryPolicy *m_entries[];
   ISF08StopPolicy *m_stops[];
   ISF08ExitPolicy *m_exits[];
   bool m_compiled;
   string m_registry_hash;

   bool IdentityExists(const string id,const string version) const
   {
      SF08_PolicyDescriptor d;
      for(int i=0;i<ArraySize(m_entries);i++){m_entries[i].Describe(d);if(d.policy_id==id && d.version==version)return true;}
      for(int i=0;i<ArraySize(m_stops);i++){m_stops[i].Describe(d);if(d.policy_id==id && d.version==version)return true;}
      for(int i=0;i<ArraySize(m_exits);i++){m_exits[i].Describe(d);if(d.policy_id==id && d.version==version)return true;}
      return false;
   }
public:
   CSF08PolicyRegistry(void){ArrayResize(m_entries,0);ArrayResize(m_stops,0);ArrayResize(m_exits,0);m_compiled=false;m_registry_hash="";}
   int EntryCount(void)const{return ArraySize(m_entries);} int StopCount(void)const{return ArraySize(m_stops);} int ExitCount(void)const{return ArraySize(m_exits);}
   bool Compiled(void)const{return m_compiled;} string RegistryHash(void)const{return m_registry_hash;}

   bool RegisterEntry(ISF08EntryPolicy *policy,string &error)
   {
      if(m_compiled){error="policy registry already compiled";return false;}
      if(CheckPointer(policy)==POINTER_INVALID){error="invalid entry policy pointer";return false;}
      SF08_PolicyDescriptor d;policy.Describe(d);if(!SF08_ValidatePolicyDescriptor(d,error))return false;
      if(d.kind!=SF08_POLICY_ENTRY){error="entry policy descriptor kind mismatch";return false;}
      if(IdentityExists(d.policy_id,d.version)){error="duplicate policy identity";return false;}
      if(ArraySize(m_entries)>=SF08_MAX_POLICY_REGISTRY){error="entry policy capacity exceeded";return false;}
      const int n=ArraySize(m_entries);ArrayResize(m_entries,n+1);m_entries[n]=policy;error="";return true;
   }
   bool RegisterStop(ISF08StopPolicy *policy,string &error)
   {
      if(m_compiled){error="policy registry already compiled";return false;}
      if(CheckPointer(policy)==POINTER_INVALID){error="invalid stop policy pointer";return false;}
      SF08_PolicyDescriptor d;policy.Describe(d);if(!SF08_ValidatePolicyDescriptor(d,error))return false;
      if(d.kind!=SF08_POLICY_STOP){error="stop policy descriptor kind mismatch";return false;}
      if(IdentityExists(d.policy_id,d.version)){error="duplicate policy identity";return false;}
      if(ArraySize(m_stops)>=SF08_MAX_POLICY_REGISTRY){error="stop policy capacity exceeded";return false;}
      const int n=ArraySize(m_stops);ArrayResize(m_stops,n+1);m_stops[n]=policy;error="";return true;
   }
   bool RegisterExit(ISF08ExitPolicy *policy,string &error)
   {
      if(m_compiled){error="policy registry already compiled";return false;}
      if(CheckPointer(policy)==POINTER_INVALID){error="invalid exit policy pointer";return false;}
      SF08_PolicyDescriptor d;policy.Describe(d);if(!SF08_ValidatePolicyDescriptor(d,error))return false;
      if(d.kind!=SF08_POLICY_EXIT){error="exit policy descriptor kind mismatch";return false;}
      if(IdentityExists(d.policy_id,d.version)){error="duplicate policy identity";return false;}
      if(ArraySize(m_exits)>=SF08_MAX_POLICY_REGISTRY){error="exit policy capacity exceeded";return false;}
      const int n=ArraySize(m_exits);ArrayResize(m_exits,n+1);m_exits[n]=policy;error="";return true;
   }

   bool Compile(string &error)
   {
      if(ArraySize(m_entries)<=0 || ArraySize(m_stops)<=0 || ArraySize(m_exits)<=0)
      {error="policy registry requires entry, stop and exit policies";return false;}
      string canonical="";SF08_PolicyDescriptor d;
      for(int i=0;i<ArraySize(m_entries);i++){m_entries[i].Describe(d);canonical+="|E|"+SF08_DerivePolicyDescriptorHash(d);}
      for(int i=0;i<ArraySize(m_stops);i++){m_stops[i].Describe(d);canonical+="|S|"+SF08_DerivePolicyDescriptorHash(d);}
      for(int i=0;i<ArraySize(m_exits);i++){m_exits[i].Describe(d);canonical+="|X|"+SF08_DerivePolicyDescriptorHash(d);}
      m_registry_hash=SF01_StableId("preg",canonical);m_compiled=true;error="";return true;
   }

   ISF08EntryPolicy *ResolveEntry(const string id,const string version) const
   {SF08_PolicyDescriptor d;for(int i=0;i<ArraySize(m_entries);i++){m_entries[i].Describe(d);if(d.policy_id==id && d.version==version)return m_entries[i];}return NULL;}
   ISF08StopPolicy *ResolveStop(const string id,const string version) const
   {SF08_PolicyDescriptor d;for(int i=0;i<ArraySize(m_stops);i++){m_stops[i].Describe(d);if(d.policy_id==id && d.version==version)return m_stops[i];}return NULL;}
   ISF08ExitPolicy *ResolveExit(const string id,const string version) const
   {SF08_PolicyDescriptor d;for(int i=0;i<ArraySize(m_exits);i++){m_exits[i].Describe(d);if(d.policy_id==id && d.version==version)return m_exits[i];}return NULL;}
};

#endif
