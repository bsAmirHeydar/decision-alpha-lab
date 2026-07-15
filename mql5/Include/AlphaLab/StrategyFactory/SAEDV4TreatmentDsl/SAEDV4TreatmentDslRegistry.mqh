#ifndef ALPHALAB_SAED_V4_TREATMENT_DSL_REGISTRY_MQH
#define ALPHALAB_SAED_V4_TREATMENT_DSL_REGISTRY_MQH

bool SAEDV4DslPrimitiveKindValid(const int kind)
  {
   return(kind>=0 && kind<=12);
  }

bool SAEDV4DslExactVersionValid(const string version)
  {
   const int first=StringFind(version,".");
   if(first<=0) return false;
   const int second=StringFind(version,".",first+1);
   return(second>first+1 && second<StringLen(version)-1);
  }

bool SAEDV4DslSystemActionValid(const string family,const int component_count)
  {
   return((family=="skip" || family=="abstain") && component_count==1);
  }
#endif
