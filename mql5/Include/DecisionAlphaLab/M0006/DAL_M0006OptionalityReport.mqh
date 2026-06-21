#ifndef __DAL_M0006_OPTIONALITY_REPORT_MQH__
#define __DAL_M0006_OPTIONALITY_REPORT_MQH__

// H0006 reuses the atomic no-sample M0001 known-time batch engine from H0004,
// but runs in H6-only mode. No M0002 samples are built and no H4 transition
// report is printed by the standalone M0006 expert.
#include <DecisionAlphaLab/M0004/DAL_M0004AtomicNoSample.mqh>

bool DAL_M0006RunReversalExplosiveOptionality(const DALM0004AtomicNoSampleConfig &config)
{
   return DAL_M0004RunAtomicNoSampleReport(config);
}

void DAL_M0006CloseReversalExplosiveOptionality()
{
   DAL_M0004CloseAtomicNoSampleReport();
}

#endif
