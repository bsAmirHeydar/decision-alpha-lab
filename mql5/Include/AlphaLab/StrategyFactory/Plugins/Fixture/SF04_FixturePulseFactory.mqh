#ifndef __SF04_FIXTURE_PULSE_FACTORY_MQH__
#define __SF04_FIXTURE_PULSE_FACTORY_MQH__
#include "../ISF04_PluginFactory.mqh"
#include "SF04_FixturePulsePlugin.mqh"
class CSF04FixturePulseFactory:public ISF04AnatomyPluginFactory{private:string m_symbol;int m_tf,m_lookback,m_ticks;public:CSF04FixturePulseFactory(void){m_symbol="EURUSD";m_tf=60;m_lookback=32;m_ticks=10;}void Configure(const string symbol,const int tf,const int lookback,const int ticks){m_symbol=symbol;m_tf=tf;m_lookback=lookback;m_ticks=ticks;}void GetDescriptor(SF04_PluginDescriptor &d)const{CSF04FixturePulsePlugin preview(m_symbol,m_tf,m_lookback,m_ticks);preview.GetDescriptor(d);}ISF04AnatomyPlugin *Create(string &e){if(!SF01_IsSafeTerminalSymbol(m_symbol)||m_tf<=0||m_lookback<2||m_ticks<1){e="invalid fixture factory configuration";return NULL;}ISF04AnatomyPlugin *p=new CSF04FixturePulsePlugin(m_symbol,m_tf,m_lookback,m_ticks);if(CheckPointer(p)==POINTER_INVALID){e="plugin allocation failed";return NULL;}e="";return p;}};
#endif
