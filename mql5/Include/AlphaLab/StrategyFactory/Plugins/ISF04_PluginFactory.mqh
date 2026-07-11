#ifndef __ISF04_PLUGIN_FACTORY_MQH__
#define __ISF04_PLUGIN_FACTORY_MQH__
#include "ISF04_AnatomyPlugin.mqh"
class ISF04AnatomyPluginFactory{public:virtual void GetDescriptor(SF04_PluginDescriptor &descriptor)const=0;virtual ISF04AnatomyPlugin *Create(string &error)=0;};
#endif
