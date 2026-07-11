#ifndef __SF05_GENERATION_BUNDLE_MQH__
#define __SF05_GENERATION_BUNDLE_MQH__
#include "SF05_GenerationCompiler.mqh"
#include "ISF05_VersionedResultSink.mqh"
class CSF05GenerationBundle
{
private:SF05_RunManifest m_manifest;SF05_RuntimeGenerationRecord m_generation;SF04_PluginDescriptor m_descriptor;ISF04AnatomyPlugin *m_plugin;ISF05VersionedResultSink *m_sink;bool m_owns_plugin;bool m_owns_sink;
public:CSF05GenerationBundle(void){m_plugin=NULL;m_sink=NULL;m_owns_plugin=false;m_owns_sink=false;}~CSF05GenerationBundle(void){Release();}
void Adopt(const SF05_RunManifest &m,const SF05_RuntimeGenerationRecord &g,const SF04_PluginDescriptor &d,ISF04AnatomyPlugin *p,ISF05VersionedResultSink *s,const bool own_plugin,const bool own_sink){Release();m_manifest=m;m_generation=g;m_descriptor=d;m_plugin=p;m_sink=s;m_owns_plugin=own_plugin;m_owns_sink=own_sink;}
void Release(void){if(m_owns_plugin&&CheckPointer(m_plugin)!=POINTER_INVALID){delete m_plugin;}if(m_owns_sink&&CheckPointer(m_sink)!=POINTER_INVALID){delete m_sink;}m_plugin=NULL;m_sink=NULL;m_owns_plugin=false;m_owns_sink=false;}
ISF04AnatomyPlugin *Plugin(void){return m_plugin;}ISF05VersionedResultSink *Sink(void){return m_sink;}SF05_RuntimeGenerationRecord Generation(void)const{return m_generation;}SF05_RunManifest Manifest(void)const{return m_manifest;}SF04_PluginDescriptor Descriptor(void)const{return m_descriptor;}void SetGeneration(const SF05_RuntimeGenerationRecord &g){m_generation=g;}bool IsValid(void)const{return CheckPointer(m_plugin)!=POINTER_INVALID&&CheckPointer(m_sink)!=POINTER_INVALID;}
};
#endif
