#ifndef __SF05_ARTIFACT_CATALOG_MQH__
#define __SF05_ARTIFACT_CATALOG_MQH__
#include "SF05_RunManifest.mqh"
struct SF05_ArtifactCatalogEntry{SF01_ArtifactIdentity identity;string relative_path;string content_type;string schema_key;bool sealed;long record_count;long byte_count;string final_hash;};
class CSF05ArtifactCatalog
{
private:SF05_ArtifactCatalogEntry m_entries[];
public:int Count(void)const{return ArraySize(m_entries);}bool Add(const SF05_ArtifactCatalogEntry &v,string &e){if(!SF01_ValidateArtifactIdentity(v.identity,e))return false;if(StringLen(v.relative_path)<=0||StringFind(v.relative_path,"..")>=0){e="invalid artifact path";return false;}for(int i=0;i<ArraySize(m_entries);i++)if(m_entries[i].identity.artifact_id==v.identity.artifact_id||m_entries[i].relative_path==v.relative_path){e="duplicate artifact";return false;}int n=ArraySize(m_entries);ArrayResize(m_entries,n+1);m_entries[n]=v;e="";return true;}bool Seal(const string artifact_id,const long records,const long bytes,const string final_hash,string &e){for(int i=0;i<ArraySize(m_entries);i++)if(m_entries[i].identity.artifact_id==artifact_id){if(m_entries[i].sealed){e="artifact already sealed";return false;}m_entries[i].sealed=true;m_entries[i].record_count=records;m_entries[i].byte_count=bytes;m_entries[i].final_hash=final_hash;e="";return true;}e="artifact not found";return false;}bool At(const int i,SF05_ArtifactCatalogEntry &v)const{if(i<0||i>=ArraySize(m_entries))return false;v=m_entries[i];return true;}};
#endif
