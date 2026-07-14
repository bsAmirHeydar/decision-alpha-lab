#ifndef __FP_I12_FILTERS_MQH__
#define __FP_I12_FILTERS_MQH__
#include "FP_I12_Contracts.mqh"
class FP_I12_FilterEngine {
 private:SFP_I12_Filter m_filter;
 public:
 void Defaults(){m_filter.show_al=true;m_filter.show_an=true;m_filter.show_ln=true;m_filter.show_na=true;m_filter.show_nl=true;m_filter.show_nn=true;m_filter.show_ww=true;m_filter.show_bullish=true;m_filter.show_bearish=true;m_filter.show_confirmed=true;m_filter.show_invalidated=true;m_filter.show_suppressed=true;m_filter.show_historical=true;m_filter.focus_semantic_id="";}
 SFP_I12_Filter Current()const{return m_filter;}
 void Set(const SFP_I12_Filter &f){m_filter=f;}
 void Reset(){Defaults();}
 bool RelationVisible(const string r)const{if(r=="AL")return m_filter.show_al;if(r=="AN")return m_filter.show_an;if(r=="LN")return m_filter.show_ln;if(r=="NA")return m_filter.show_na;if(r=="NL")return m_filter.show_nl;if(r=="NN")return m_filter.show_nn;if(r=="WW")return m_filter.show_ww;return true;}
 bool DirectionVisible(const string d)const{if(d=="BULLISH")return m_filter.show_bullish;if(d=="BEARISH")return m_filter.show_bearish;return true;}
 bool FocusVisible(const string id)const{return m_filter.focus_semantic_id==""||m_filter.focus_semantic_id==id;}
};
#endif
