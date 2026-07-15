#ifndef ALPHA_LAB_SAED_V4_HYPERGRAPH_TEMPORAL_MQH
#define ALPHA_LAB_SAED_V4_HYPERGRAPH_TEMPORAL_MQH

bool SAEDHypergraphBoundaryVisible(const datetime event_time,
                                   const datetime known_time,
                                   const datetime event_as_of,
                                   const datetime known_as_of)
  {
   if(event_time>event_as_of)
      return false;
   if(known_time>known_as_of)
      return false;
   if(known_time<event_time)
      return false;
   return true;
  }

bool SAEDHypergraphIntervalValid(const datetime start_time,
                                 const datetime end_time,
                                 const datetime known_time,
                                 const datetime event_as_of,
                                 const datetime known_as_of)
  {
   if(start_time>end_time)
      return false;
   return SAEDHypergraphBoundaryVisible(end_time,known_time,event_as_of,known_as_of);
  }

#endif
