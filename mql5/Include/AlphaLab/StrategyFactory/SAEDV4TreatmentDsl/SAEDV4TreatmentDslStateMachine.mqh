#ifndef ALPHALAB_SAED_V4_TREATMENT_DSL_STATE_MACHINE_MQH
#define ALPHALAB_SAED_V4_TREATMENT_DSL_STATE_MACHINE_MQH

bool SAEDV4DslTransitionValid(const int from_index,const int to_index,const int state_count)
  {
   if(state_count<1) return false;
   if(from_index<0 || to_index<0 || from_index>=state_count || to_index>=state_count) return false;
   return(from_index!=to_index);
  }

bool SAEDV4DslAcyclicTopologicalCountValid(const int visited_count,const int state_count)
  {
   return(state_count>=0 && visited_count==state_count);
  }
#endif
