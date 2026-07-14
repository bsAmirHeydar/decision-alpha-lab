#ifndef __FP_I12_PREFERENCES_MQH__
#define __FP_I12_PREFERENCES_MQH__
#include "FP_I12_Contracts.mqh"
#include "FP_I12_Hash.mqh"
class FP_I12_Preferences {private:string m_key;public:void Initialize(const string instance_id){m_key="FP12.PREF."+FP_I12_Hash(instance_id);}void SaveMode(const int mode){GlobalVariableSet(m_key+".MODE",mode);}int LoadMode(const int fallback)const{return GlobalVariableCheck(m_key+".MODE")?(int)GlobalVariableGet(m_key+".MODE"):fallback;}void SavePage(const int page){GlobalVariableSet(m_key+".PAGE",page);}int LoadPage()const{return GlobalVariableCheck(m_key+".PAGE")?(int)GlobalVariableGet(m_key+".PAGE"):0;}void SaveFilterMask(const int mask){GlobalVariableSet(m_key+".FILTER",mask);}int LoadFilterMask(const int fallback)const{return GlobalVariableCheck(m_key+".FILTER")?(int)GlobalVariableGet(m_key+".FILTER"):fallback;}};
#endif
