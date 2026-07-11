#ifndef __SF20_EXP0017_FACTORY_MQH__
#define __SF20_EXP0017_FACTORY_MQH__
#include "SF20_EXP0017Plugin.mqh"
#include "../../Plugins/ISF04_PluginFactory.mqh"
class CSF20EXP0017Factory:public ISF04AnatomyPluginFactory
{
private:SF20_EXP0017Config m_config;
public:CSF20EXP0017Factory(){m_config=SF20_DefaultEXP0017Config();}void Configure(const SF20_EXP0017Config &c){m_config=c;}void GetDescriptor(SF04_PluginDescriptor &d)const{CSF20EXP0017Plugin p(m_config);p.GetDescriptor(d);}ISF04AnatomyPlugin *Create(string &error){if(!SF20_ValidateEXP0017Config(m_config,error))return NULL;ISF04AnatomyPlugin *p=new CSF20EXP0017Plugin(m_config);if(CheckPointer(p)==POINTER_INVALID){error="EXP0017 plugin allocation failed";return NULL;}error="";return p;}
};
#endif
