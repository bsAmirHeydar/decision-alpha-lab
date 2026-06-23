#ifndef __DAL_EXPERIMENT_CONFIG_MQH__
#define __DAL_EXPERIMENT_CONFIG_MQH__

struct DALExperimentIdentity
{
   string experiment_id;
   string hypothesis_id;
   string symbol;
   ENUM_TIMEFRAMES timeframe;
   string notes;
};

#endif
