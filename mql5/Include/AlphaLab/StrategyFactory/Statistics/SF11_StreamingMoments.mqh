#ifndef __SF11_STREAMING_MOMENTS_MQH__
#define __SF11_STREAMING_MOMENTS_MQH__
#include "SF11_StatisticalSample.mqh"
class CSF11StreamingMoments
{
private:
   long m_count;double m_mean;double m_m2;double m_minimum;double m_maximum;
public:
   CSF11StreamingMoments(){Reset();}
   void Reset(void){m_count=0;m_mean=0.0;m_m2=0.0;m_minimum=DBL_MAX;m_maximum=-DBL_MAX;}
   bool Add(const double value)
   {
      if(!MathIsValidNumber(value))return false;
      m_count++;const double delta=value-m_mean;m_mean+=delta/(double)m_count;
      m_m2+=delta*(value-m_mean);if(value<m_minimum)m_minimum=value;if(value>m_maximum)m_maximum=value;return true;
   }
   long Count(void) const{return m_count;}
   double Mean(void) const{return m_mean;}
   double Variance(void) const{return (m_count>1)?m_m2/(double)(m_count-1):0.0;}
   double StandardDeviation(void) const{return MathSqrt(MathMax(0.0,Variance()));}
   double StandardError(void) const{return (m_count>0)?StandardDeviation()/MathSqrt((double)m_count):0.0;}
   double Minimum(void) const{return (m_count>0)?m_minimum:0.0;}
   double Maximum(void) const{return (m_count>0)?m_maximum:0.0;}
};
class CSF11DrawdownTracker
{
private:double m_equity;double m_peak;double m_trough;double m_max_drawdown;double m_max_runup;
public:
   CSF11DrawdownTracker(){Reset();}
   void Reset(void){m_equity=0.0;m_peak=0.0;m_trough=0.0;m_max_drawdown=0.0;m_max_runup=0.0;}
   void Add(const double value){m_equity+=value;if(m_equity>m_peak)m_peak=m_equity;
      const double dd=m_peak-m_equity;if(dd>m_max_drawdown)m_max_drawdown=dd;
      if(m_equity<m_trough)m_trough=m_equity;const double ru=m_equity-m_trough;if(ru>m_max_runup)m_max_runup=ru;}
   double MaximumDrawdown(void) const{return m_max_drawdown;}
   double MaximumRunup(void) const{return m_max_runup;}
};
#endif
