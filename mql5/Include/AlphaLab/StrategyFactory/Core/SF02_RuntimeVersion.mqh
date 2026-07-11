#ifndef __SF02_RUNTIME_VERSION_MQH__
#define __SF02_RUNTIME_VERSION_MQH__

#define SF02_RUNTIME_MAJOR 1
#define SF02_RUNTIME_MINOR 0
#define SF02_RUNTIME_PATCH 0
#define SF02_RUNTIME_NAME  "strategy_factory_runtime"

string SF02_RuntimeVersion()
{
   return IntegerToString(SF02_RUNTIME_MAJOR) + "." +
          IntegerToString(SF02_RUNTIME_MINOR) + "." +
          IntegerToString(SF02_RUNTIME_PATCH);
}

#endif
