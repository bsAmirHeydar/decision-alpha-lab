#ifndef ALPHALAB_SAED_V4_TREATMENT_DSL_PARAMETERS_MQH
#define ALPHALAB_SAED_V4_TREATMENT_DSL_PARAMETERS_MQH

bool SAEDV4DslDecimalInRange(const double value,const double minimum_value,const double maximum_value)
  {
   if(!MathIsValidNumber(value)) return false;
   return(value>=minimum_value && value<=maximum_value);
  }

bool SAEDV4DslDurationIsValid(const long duration_ms,const long maximum_ms)
  {
   return(duration_ms>=0 && duration_ms<=maximum_ms);
  }

bool SAEDV4DslFractionIsValid(const double value)
  {
   return SAEDV4DslDecimalInRange(value,0.0,1.0);
  }
#endif
