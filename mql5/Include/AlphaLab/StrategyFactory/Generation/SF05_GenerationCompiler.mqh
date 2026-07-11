#ifndef __SF05_GENERATION_COMPILER_MQH__
#define __SF05_GENERATION_COMPILER_MQH__
#include "SF05_RuntimeGeneration.mqh"
#include "../Plugins/SF04_PluginRegistry.mqh"
#include "../Plugins/SF04_PluginStartupValidator.mqh"

struct SF05_CompilationReport
{
   bool success;
   string generation_uid;
   string manifest_hash;
   string descriptor_hash;
   string requirements_hash;
   string sink_config_hash;
   string detail;
};

class CSF05GenerationCompiler
{
private:
   CSF04PluginRegistry *m_registry;CSF04PluginStartupValidator *m_validator;ISF02ClockPort *m_clock;CSF03MarketDataService *m_market;CSF03SymbolSpecCache *m_specs;
public:
   CSF05GenerationCompiler(void){m_registry=NULL;m_validator=NULL;m_clock=NULL;m_market=NULL;m_specs=NULL;}
   void Bind(CSF04PluginRegistry *r,CSF04PluginStartupValidator *v,ISF02ClockPort *c,CSF03MarketDataService *m,CSF03SymbolSpecCache *s){m_registry=r;m_validator=v;m_clock=c;m_market=m;m_specs=s;}
   bool Compile(SF05_RunManifest &manifest,ISF04AnatomyPlugin *&plugin,SF04_PluginDescriptor &descriptor,SF04_StartupValidationReport &startup,SF05_RuntimeGenerationRecord &generation,SF05_CompilationReport &report,string &e)
   {
      plugin=NULL;report.success=false;report.detail="";
      if(CheckPointer(m_registry)==POINTER_INVALID||CheckPointer(m_validator)==POINTER_INVALID||CheckPointer(m_clock)==POINTER_INVALID||CheckPointer(m_market)==POINTER_INVALID||CheckPointer(m_specs)==POINTER_INVALID){e="compiler not bound";return false;}
      if(manifest.manifest_id=="")manifest.manifest_id=SF05_DeriveRunManifestId(manifest);
      if(!SF05_ValidateRunManifest(manifest,e))return false;
      if(!m_registry.Create(manifest.plugin_selection,plugin,descriptor,e))return false;
      if(!plugin.BindSharedServices(m_clock,m_market,m_specs,e)){delete plugin;plugin=NULL;return false;}
      if(!m_validator.ValidateAndPrepare(plugin,startup,e)){delete plugin;plugin=NULL;return false;}
      generation.schema="alpha_lab.strategy_factory/runtime_generation@1.0.0";
      generation.generation_uid="";generation.generation_id=manifest.requested_generation_id;generation.state=SF05_GENERATION_DRAFT;generation.run_manifest_id=manifest.manifest_id;generation.run_manifest_hash=SF01_StableId("mnh",SF05_RunManifestCanonical(manifest));generation.plugin_descriptor_hash=SF04_PluginDescriptorHash(descriptor);generation.plugin_requirements_hash=startup.requirements_hash;generation.plugin_configuration_hash=manifest.plugin_configuration_hash;generation.market_configuration_hash=manifest.market_configuration_hash;generation.sink_configuration_hash=SF05_ResultSinkConfigHash(manifest.sink_config);generation.compiler_id="sf05.generation_compiler";generation.compiler_version="1.0.0";generation.previous_generation_uid="";generation.compiled_at=SF01_MakeUtcMilliseconds(m_clock.UtcNowMilliseconds(),"UTC",0,"sf05_compiler",SF01_TIME_MILLISECONDS);generation.activated_at=SF01_MakeUtcMilliseconds(0,"UTC",0,"sf05_compiler",SF01_TIME_MILLISECONDS);generation.retired_at=SF01_MakeUtcMilliseconds(0,"UTC",0,"sf05_compiler",SF01_TIME_MILLISECONDS);generation.failure_reason="";
      if(!SF05_TransitionGeneration(generation,SF05_GENERATION_COMPILED,generation.compiled_at,"compiled",e)){delete plugin;plugin=NULL;return false;}
      generation.generation_uid=SF05_DeriveGenerationUid(generation);
      if(!SF05_ValidateRuntimeGeneration(generation,e)){delete plugin;plugin=NULL;return false;}
      if(!SF05_TransitionGeneration(generation,SF05_GENERATION_VALIDATED,generation.compiled_at,"validated",e)){delete plugin;plugin=NULL;return false;}
      if(!SF05_TransitionGeneration(generation,SF05_GENERATION_WARMED,generation.compiled_at,"warmed",e)){delete plugin;plugin=NULL;return false;}
      report.success=true;report.generation_uid=generation.generation_uid;report.manifest_hash=generation.run_manifest_hash;report.descriptor_hash=generation.plugin_descriptor_hash;report.requirements_hash=generation.plugin_requirements_hash;report.sink_config_hash=generation.sink_configuration_hash;report.detail="WARMED";e="";return true;
   }
};
#endif
