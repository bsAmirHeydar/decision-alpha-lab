#ifndef __UCE02_REGISTRY_MQH__
#define __UCE02_REGISTRY_MQH__
#include "UCE02_ContextPackage.mqh"
class CUCE02StaticPackageRegistry{
private:IUCE02ContextPackage *m_packages[];bool m_owned[];
public:CUCE02StaticPackageRegistry(){ArrayResize(m_packages,0);ArrayResize(m_owned,0);}~CUCE02StaticPackageRegistry(){Clear();}void Clear(){for(int i=0;i<ArraySize(m_packages);i++)if(m_owned[i]&&CheckPointer(m_packages[i])!=POINTER_INVALID)delete m_packages[i];ArrayResize(m_packages,0);ArrayResize(m_owned,0);}bool Register(IUCE02ContextPackage *package,const bool take_ownership,string &error){if(CheckPointer(package)==POINTER_INVALID){error="invalid context package pointer";return false;}UCE02_ContextPackageManifest candidate;package.GetManifest(candidate);for(int i=0;i<ArraySize(m_packages);i++){UCE02_ContextPackageManifest existing;m_packages[i].GetManifest(existing);if(existing.package_id==candidate.package_id&&existing.version==candidate.version){error="duplicate exact context package version";return false;}}if(!package.ValidatePackage(error))return false;int n=ArraySize(m_packages);ArrayResize(m_packages,n+1);ArrayResize(m_owned,n+1);m_packages[n]=package;m_owned[n]=take_ownership;error="";return true;}IUCE02ContextPackage *Resolve(const string id,const string version)const{for(int i=0;i<ArraySize(m_packages);i++){UCE02_ContextPackageManifest item;m_packages[i].GetManifest(item);if(item.package_id==id&&item.version==version)return m_packages[i];}return NULL;}int Count()const{return ArraySize(m_packages);}
};
#endif
