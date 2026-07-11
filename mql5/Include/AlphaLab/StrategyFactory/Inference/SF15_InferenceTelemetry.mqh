#ifndef __SF15_INFERENCE_TELEMETRY_MQH__
#define __SF15_INFERENCE_TELEMETRY_MQH__
struct SF15_InferenceTelemetry
  {
   long startup_attempts,startup_failures,requests_received,requests_rejected,runtime_failures,accepted_results,total_latency_micros,max_latency_micros;
   void Reset(){startup_attempts=0;startup_failures=0;requests_received=0;requests_rejected=0;runtime_failures=0;accepted_results=0;total_latency_micros=0;max_latency_micros=0;}
   double MeanLatencyMicros()const{return accepted_results>0?(double)total_latency_micros/(double)accepted_results:0.0;}
  };
#endif
