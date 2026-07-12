#ifndef __UCE03_SCHEMA_REGISTRY_MQH__
#define __UCE03_SCHEMA_REGISTRY_MQH__
#include "UCE03_Schema.mqh"
class CUCE03SchemaRegistry
{
private:
   UCE03_SchemaDescriptor m_items[];
public:
   bool Register(const UCE03_SchemaDescriptor &descriptor,string &error)
   {
      const string key=UCE03_SchemaExactKey(descriptor.schema_id);
      for(int i=0;i<ArraySize(m_items);i++)if(UCE03_SchemaExactKey(m_items[i].schema_id)==key)
      {
         if(m_items[i].semantic_hash_sha256!=descriptor.semantic_hash_sha256){error="exact schema redefinition";return false;}
         error="";return true;
      }
      const int size=ArraySize(m_items);ArrayResize(m_items,size+1);m_items[size]=descriptor;error="";return true;
   }
   bool ResolveExact(const UCE03_SchemaId &schema_id,UCE03_SchemaDescriptor &out)
   {
      const string key=UCE03_SchemaExactKey(schema_id);
      for(int i=0;i<ArraySize(m_items);i++)if(UCE03_SchemaExactKey(m_items[i].schema_id)==key){out=m_items[i];return true;}
      return false;
   }
   bool SupportsMajor(const string schema_namespace,const string name,const int major)
   {
      for(int i=0;i<ArraySize(m_items);i++)if(m_items[i].schema_id.schema_namespace==schema_namespace&&m_items[i].schema_id.name==name&&m_items[i].schema_id.version.major==major)return true;
      return false;
   }
   int Count(){return ArraySize(m_items);}
};
#endif
