#ifndef __SF02_SERVICE_HEALTH_MQH__
#define __SF02_SERVICE_HEALTH_MQH__

#include "SF02_RuntimeEnums.mqh"

struct SF02_ServiceHealth
{
   string service_id;
   ENUM_SF02_SERVICE_KIND service_kind;
   ENUM_SF02_HEALTH_STATUS status;
   string detail;
   long observed_at_utc_msc;
};

#endif
