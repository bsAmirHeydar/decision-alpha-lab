#ifndef __FP_I14_INDICATOR_PROBE_MQH__
#define __FP_I14_INDICATOR_PROBE_MQH__
class CFP_I14_IndicatorProbe {
 private: int m_handle;
 public:
  CFP_I14_IndicatorProbe(){m_handle=INVALID_HANDLE;}
  bool Open(const string primary,const string secondary,const ENUM_TIMEFRAMES host_tf){ m_handle=iCustom(primary,PERIOD_M1,"EXP0019\\FaerieProtocol\\EXP0019_FaerieProtocol_Context",primary,secondary,"FP-EPOCH-1",host_tf); return m_handle!=INVALID_HANDLE; }
  bool ReadBufferValue(const int buffer_index,const int shift,double &value){ if(m_handle==INVALID_HANDLE)return false;double data[1];if(CopyBuffer(m_handle,buffer_index,shift,1,data)!=1)return false;value=data[0];return true; }
  void Close(){if(m_handle!=INVALID_HANDLE){IndicatorRelease(m_handle);m_handle=INVALID_HANDLE;}}
};
#endif
