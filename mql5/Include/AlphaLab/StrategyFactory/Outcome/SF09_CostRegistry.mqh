#ifndef __SF09_COST_REGISTRY_MQH__
#define __SF09_COST_REGISTRY_MQH__
#include "SF09_CostModel.mqh"

class CSF09CostRegistry
{
private:
   ISF09CostModel *m_models[SF09_MAX_COST_MODELS];
   SF09_CostModelDescriptor m_descriptors[SF09_MAX_COST_MODELS];
   int m_count;
   bool m_compiled;
   string m_registry_hash;
public:
   CSF09CostRegistry(void){m_count=0;m_compiled=false;m_registry_hash="";for(int i=0;i<SF09_MAX_COST_MODELS;i++)m_models[i]=NULL;}
   bool Register(ISF09CostModel *model,string &error)
   {
      if(m_compiled){error="cost registry already compiled";return false;}
      if(model==NULL||m_count>=SF09_MAX_COST_MODELS){error="invalid cost model or capacity";return false;}
      SF09_CostModelDescriptor d;if(!model.Descriptor(d)){error="cost model descriptor failed";return false;}
      if(!SF01_IsSafeIdentifier(d.model_id,128)||!SF01_IsSafeIdentifier(d.version,64)){error="invalid cost model identity";return false;}
      for(int i=0;i<m_count;i++)if(m_descriptors[i].model_id==d.model_id&&m_descriptors[i].version==d.version){error="duplicate cost model";return false;}
      m_models[m_count]=model;m_descriptors[m_count]=d;m_count++;error="";return true;
   }
   bool Compile(string &error)
   {
      if(m_count<=0){error="empty cost registry";return false;}
      string canonical="";
      for(int i=0;i<m_count;i++)canonical+=m_descriptors[i].model_id+"@"+m_descriptors[i].version+"|"+m_descriptors[i].descriptor_hash+";";
      m_registry_hash=SF01_StableId("creg",canonical);m_compiled=true;error="";return true;
   }
   ISF09CostModel *Resolve(const string model_id,const string version) const
   {
      if(!m_compiled)return NULL;
      for(int i=0;i<m_count;i++)if(m_descriptors[i].model_id==model_id&&m_descriptors[i].version==version)return m_models[i];
      return NULL;
   }
   string RegistryHash(void) const{return m_registry_hash;}
   int Count(void) const{return m_count;}
};

#endif
