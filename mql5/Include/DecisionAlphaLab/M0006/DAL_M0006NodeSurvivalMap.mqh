#ifndef __DAL_M0006_NODE_SURVIVAL_MAP_MQH__
#define __DAL_M0006_NODE_SURVIVAL_MAP_MQH__

// H0006 official structure after release 111:
// raw M0001 nodes become visual edge candidates when their node price is not
// broken after 20/50/100 closed candles from known-time. No M0002 samples and
// no same-candle ordering are introduced.
#include <DecisionAlphaLab/M0004/DAL_M0004AtomicNoSample.mqh>

bool DAL_M0006RunNodeSurvivalMap(const DALM0004AtomicNoSampleConfig &config)
{
   return DAL_M0004RunAtomicNoSampleReport(config);
}

void DAL_M0006CloseNodeSurvivalMap()
{
   DAL_M0004CloseAtomicNoSampleReport();
}

#endif
