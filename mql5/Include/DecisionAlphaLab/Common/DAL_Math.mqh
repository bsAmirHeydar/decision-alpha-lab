#ifndef __DAL_MATH_MQH__
#define __DAL_MATH_MQH__

double DAL_SafeDiv(const double numerator, const double denominator, const double fallback = 0.0)
{
   if(MathAbs(denominator) <= DBL_EPSILON)
      return fallback;
   return numerator / denominator;
}

double DAL_LogRange(const double high, const double low)
{
   double range = MathAbs(high - low);
   if(range <= 0.0)
      return 0.0;
   return MathLog(range);
}

double DAL_MeanRangeLog(const double &values[], const int start, const int count)
{
   if(count <= 0)
      return 0.0;

   double total = 0.0;
   int used = 0;
   int n = ArraySize(values);

   for(int i = 0; i < count; i++)
   {
      int idx = start + i;
      if(idx < 0 || idx >= n)
         continue;
      total += values[idx];
      used++;
   }

   if(used <= 0)
      return 0.0;
   return total / used;
}

bool DAL_CandleIntersectsZone(const double low, const double high, const double lower, const double upper)
{
   return (high >= lower && low <= upper);
}

#endif
