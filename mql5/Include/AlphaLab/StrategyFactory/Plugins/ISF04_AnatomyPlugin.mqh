#ifndef __ISF04_ANATOMY_PLUGIN_MQH__
#define __ISF04_ANATOMY_PLUGIN_MQH__
#include "../Ports/ISF02_AnatomyProvider.mqh"
#include "../Ports/ISF02_ClockPort.mqh"
#include "../Market/SF03_MarketDataService.mqh"
#include "../Market/SF03_SymbolSpecCache.mqh"
#include "SF04_PluginDescriptor.mqh"
#include "SF04_DataRequirement.mqh"
#include "SF04_PluginTelemetry.mqh"
class ISF04AnatomyPlugin:public ISF02AnatomyProvider{public:virtual void GetDescriptor(SF04_PluginDescriptor &descriptor)const=0;virtual string DescriptorHash(void)const=0;virtual int RequirementCount(void)const=0;virtual bool GetRequirement(const int index,SF04_DataRequirement &requirement)const=0;virtual bool BindSharedServices(ISF02ClockPort *clock,CSF03MarketDataService *market,CSF03SymbolSpecCache *specs,string &error)=0;virtual bool ValidatePluginConfiguration(string &error)const=0;virtual ENUM_SF04_PLUGIN_STATUS PluginStatus(void)const=0;virtual SF04_PluginTelemetrySnapshot PluginTelemetry(void)const=0;};
#endif
