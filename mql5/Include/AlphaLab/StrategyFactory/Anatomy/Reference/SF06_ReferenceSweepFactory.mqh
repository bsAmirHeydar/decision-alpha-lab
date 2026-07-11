#ifndef __SF06_REFERENCE_SWEEP_FACTORY_MQH__
#define __SF06_REFERENCE_SWEEP_FACTORY_MQH__
#include "../../Plugins/ISF04_PluginFactory.mqh"
#include "SF06_ReferenceSweepPlugin.mqh"
class CSF06ReferenceSweepFactory:public ISF04AnatomyPluginFactory
{
private:string m_symbol;int m_tf,m_lookback;double m_min_points;bool m_require_inside;
public:CSF06ReferenceSweepFactory(void){m_symbol="EURUSD";m_tf=60;m_lookback=64;m_min_points=1.0;m_require_inside=true;}void Configure(const string s,const int tf,const int lb,const double mp,const bool ri){m_symbol=s;m_tf=tf;m_lookback=lb;m_min_points=mp;m_require_inside=ri;}void GetDescriptor(SF04_PluginDescriptor &d)const{CSF06ReferenceSweepPlugin p(m_symbol,m_tf,m_lookback,m_min_points,m_require_inside);p.GetDescriptor(d);}ISF04AnatomyPlugin *Create(string &e){if(!SF01_IsSafeTerminalSymbol(m_symbol,64)||m_tf<=0||m_lookback<3||m_min_points<0){e="invalid reference anatomy configuration";return NULL;}ISF04AnatomyPlugin *p=new CSF06ReferenceSweepPlugin(m_symbol,m_tf,m_lookback,m_min_points,m_require_inside);if(CheckPointer(p)==POINTER_INVALID){e="plugin allocation failed";return NULL;}e="";return p;}
};
#endif
