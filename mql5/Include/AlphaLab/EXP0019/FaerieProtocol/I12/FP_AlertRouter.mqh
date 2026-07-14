#ifndef __FP_ALERT_ROUTER_MQH__
#define __FP_ALERT_ROUTER_MQH__
#include "FP_I12_Contracts.mqh"
#include "FP_I12_Hash.mqh"
class FP_I12_AlertRouter {
 private:SFP_I12_Config m_cfg;string m_ids[];int m_minute;int m_count;long m_delivered;long m_suppressed;int FindId(const string id)const{for(int i=0;i<ArraySize(m_ids);i++)if(m_ids[i]==id)return i;return -1;}
 public:
 FP_I12_AlertRouter(){m_minute=-1;m_count=0;m_delivered=0;m_suppressed=0;}
 void Initialize(const SFP_I12_Config &cfg){m_cfg=cfg;ArrayResize(m_ids,0);}
 bool Route(const SFP_I12_AlertCandidate &c){if(!m_cfg.alerts_enabled){m_suppressed++;return false;}if(m_cfg.suppress_historical&&(c.historical||c.event_time<m_cfg.startup_watermark)){m_suppressed++;return false;}if(FindId(c.alert_id)>=0){m_suppressed++;return false;}int minute=(int)(c.event_time/60);if(minute!=m_minute){m_minute=minute;m_count=0;}if(m_count>=m_cfg.max_alerts_per_minute){m_suppressed++;return false;}ArrayResize(m_ids,ArraySize(m_ids)+1);m_ids[ArraySize(m_ids)-1]=c.alert_id;m_count++;string msg=c.title+" | "+c.message;if(m_cfg.alert_popup)Alert(msg);if(m_cfg.alert_sound)PlaySound("alert.wav");if(m_cfg.alert_push)SendNotification(msg);if(m_cfg.alert_email)SendMail("Faerie Protocol",msg);Print("FP-I12 ALERT ",msg);m_delivered++;return true;}
 void AcknowledgeAll(){}long Delivered()const{return m_delivered;}long Suppressed()const{return m_suppressed;}
};
#endif
