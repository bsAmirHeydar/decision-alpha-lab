#ifndef __UCE03_MIGRATION_MQH__
#define __UCE03_MIGRATION_MQH__
#include "UCE03_SchemaRegistry.mqh"
#include "UCE03_KnownTime.mqh"
struct UCE03_MigrationEdge
{
   string migration_id;
   UCE03_SchemaId source;
   UCE03_SchemaId destination;
   string source_semantic_hash_sha256;
   string destination_semantic_hash_sha256;
   string migration_mode;
};
struct UCE03_MigrationEvidence
{
   string migration_path_csv;
   string source_schema_id;
   string destination_schema_id;
   string source_payload_sha256;
   string destination_payload_sha256;
   UCE03_UtcInstant applied_at;
};
class CUCE03MigrationRegistry
{
private:
   UCE03_MigrationEdge m_edges[];
public:
   bool Register(const UCE03_MigrationEdge &edge,CUCE03SchemaRegistry &schemas,string &error)
   {
      if(UCE03_SchemaFamily(edge.source)!=UCE03_SchemaFamily(edge.destination)){error="cross-family migration";return false;}
      if(UCE03_CompareVersion(edge.source.version,edge.destination.version)>=0){error="migration must be monotonic";return false;}
      UCE03_SchemaDescriptor source;UCE03_SchemaDescriptor destination;
      if(!schemas.ResolveExact(edge.source,source)||!schemas.ResolveExact(edge.destination,destination)){error="migration references unknown exact schema";return false;}
      if(source.semantic_hash_sha256!=edge.source_semantic_hash_sha256||destination.semantic_hash_sha256!=edge.destination_semantic_hash_sha256){error="migration semantic hash mismatch";return false;}
      for(int i=0;i<ArraySize(m_edges);i++)if(m_edges[i].migration_id==edge.migration_id){error="duplicate migration_id";return false;}
      const int size=ArraySize(m_edges);ArrayResize(m_edges,size+1);m_edges[size]=edge;error="";return true;
   }
   bool FindDirect(const UCE03_SchemaId &source,const UCE03_SchemaId &destination,UCE03_MigrationEdge &out)
   {
      for(int i=0;i<ArraySize(m_edges);i++)if(UCE03_SchemaExactEqual(m_edges[i].source,source)&&UCE03_SchemaExactEqual(m_edges[i].destination,destination)){out=m_edges[i];return true;}
      return false;
   }
   bool FindDirectToCsv(const UCE03_SchemaId &source,const string destination_schema_ids_csv,UCE03_MigrationEdge &out)
   {
      for(int i=0;i<ArraySize(m_edges);i++)
      {
         if(!UCE03_SchemaExactEqual(m_edges[i].source,source))continue;
         if(StringFind(","+destination_schema_ids_csv+",",","+UCE03_SchemaExactKey(m_edges[i].destination)+",")>=0){out=m_edges[i];return true;}
      }
      return false;
   }
   int Count(){return ArraySize(m_edges);}
};
#endif
