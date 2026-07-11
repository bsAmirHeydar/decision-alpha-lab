#ifndef __SF11_BOUNDED_QUANTILES_MQH__
#define __SF11_BOUNDED_QUANTILES_MQH__
#include "SF11_StreamingMoments.mqh"
class CSF11BoundedQuantiles
{
private:
   double m_values[];int m_capacity;long m_seen;
   void SortValues(void){const int n=ArraySize(m_values);for(int i=1;i<n;i++){double v=m_values[i];int j=i-1;while(j>=0&&m_values[j]>v){m_values[j+1]=m_values[j];j--;}m_values[j+1]=v;}}
public:
   CSF11BoundedQuantiles(){m_capacity=4096;m_seen=0;ArrayResize(m_values,0);}
   bool Configure(const int capacity){if(capacity<16)return false;m_capacity=capacity;m_seen=0;ArrayResize(m_values,0);return true;}
   bool Add(const double value)
   {
      if(!MathIsValidNumber(value))return false;m_seen++;int n=ArraySize(m_values);
      if(n<m_capacity){ArrayResize(m_values,n+1);m_values[n]=value;SortValues();return true;}
      const int slot=(int)((m_seen*(long)2654435761)%m_capacity);m_values[slot]=value;SortValues();return true;
   }
   double Quantile(const double q) const
   {
      const int n=ArraySize(m_values);if(n==0)return 0.0;double qq=MathMax(0.0,MathMin(1.0,q));
      const double pos=qq*(double)(n-1);const int lo=(int)MathFloor(pos);const int hi=(int)MathCeil(pos);
      if(lo==hi)return m_values[lo];return m_values[lo]+(m_values[hi]-m_values[lo])*(pos-(double)lo);
   }
};
#endif
