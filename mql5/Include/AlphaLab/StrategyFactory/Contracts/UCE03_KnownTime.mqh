#ifndef __UCE03_KNOWN_TIME_MQH__
#define __UCE03_KNOWN_TIME_MQH__
#include "UCE03_CanonicalCodec.mqh"
struct UCE03_UtcInstant
{
   long epoch_ms;
   string clock_id;
};
struct UCE03_KnownTimeChain
{
   UCE03_UtcInstant event_time;
   UCE03_UtcInstant known_time;
   UCE03_UtcInstant confirmation_time;
   UCE03_UtcInstant observation_cut;
   UCE03_UtcInstant decision_time;
   bool has_action_time;
   UCE03_UtcInstant action_time;
   bool has_fill_time;
   UCE03_UtcInstant fill_time;
   bool has_label_maturity_time;
   UCE03_UtcInstant label_maturity_time;
};
UCE03_UtcInstant UCE03_MakeUtcInstant(const long epoch_ms,const string clock_id)
{
   UCE03_UtcInstant value;value.epoch_ms=epoch_ms;value.clock_id=clock_id;return value;
}
bool UCE03_ValidateUtcInstant(const UCE03_UtcInstant &value,string &error)
{
   if(value.epoch_ms<0){error="negative UTC epoch milliseconds";return false;}
   if(value.clock_id==""){error="clock_id is required";return false;}
   error="";return true;
}
bool UCE03_ValidateKnownTimeChain(const UCE03_KnownTimeChain &value,string &error)
{
   if(value.event_time.epoch_ms>value.known_time.epoch_ms){error="known_time precedes event_time";return false;}
   if(value.known_time.epoch_ms>value.confirmation_time.epoch_ms){error="confirmation_time precedes known_time";return false;}
   if(value.confirmation_time.epoch_ms>value.observation_cut.epoch_ms){error="observation_cut precedes confirmation_time";return false;}
   if(value.observation_cut.epoch_ms>value.decision_time.epoch_ms){error="decision_time precedes observation_cut";return false;}
   long cursor=value.decision_time.epoch_ms;
   if(value.has_action_time){if(value.action_time.epoch_ms<cursor){error="action_time precedes decision_time";return false;}cursor=value.action_time.epoch_ms;}
   if(value.has_fill_time)
   {
      if(!value.has_action_time){error="fill_time requires action_time";return false;}
      if(value.fill_time.epoch_ms<cursor){error="fill_time precedes action_time";return false;}cursor=value.fill_time.epoch_ms;
   }
   if(value.has_label_maturity_time && value.label_maturity_time.epoch_ms<cursor){error="label_maturity_time precedes previous stage";return false;}
   error="";return true;
}
bool UCE03_FeatureKnownByCut(const UCE03_KnownTimeChain &chain,const long feature_known_ms)
{return feature_known_ms<=chain.observation_cut.epoch_ms;}
string UCE03_UtcInstantToJson(const UCE03_UtcInstant &value)
{
   CUCE03CanonicalObject object;object.AddString("clock_id",value.clock_id);object.AddLong("epoch_ms",value.epoch_ms);object.AddString("timezone","UTC");return object.Serialize();
}
#endif
