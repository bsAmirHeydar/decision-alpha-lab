#ifndef __SF10_OPTIMIZATION_FRAMES_MQH__
#define __SF10_OPTIMIZATION_FRAMES_MQH__
#include "SF10_PassSummary.mqh"

bool SF10_SendOptimizationFrame(const SF10_PassSummary &summary,string &error)
{
   double data[];SF10_PassSummaryToFrame(summary,data);
   ResetLastError();
   if(!FrameAdd("sf10.pass",summary.public_id,summary.objective_score,data))
   {error="FrameAdd failed: "+IntegerToString(GetLastError());return false;}
   error="";return true;
}

bool SF10_ReadNextOptimizationFrame(ulong &pass,string &name,long &public_id,double &value,double &data[],string &error)
{
   ResetLastError();
   if(!FrameNext(pass,name,public_id,value,data))
   {
      const int code=GetLastError();
      if(code!=0)error="FrameNext failed: "+IntegerToString(code);else error="";
      return false;
   }
   error="";return true;
}
#endif
