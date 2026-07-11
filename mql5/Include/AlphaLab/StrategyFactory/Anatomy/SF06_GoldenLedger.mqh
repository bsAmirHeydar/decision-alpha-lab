#ifndef __SF06_GOLDEN_LEDGER_MQH__
#define __SF06_GOLDEN_LEDGER_MQH__
#include "SF06_EventBuilder.mqh"
struct SF06_GoldenExpectation{string case_id;string expected_observation_id;string expected_event_id;ENUM_SF01_DIRECTION expected_direction;double expected_reference_price;double expected_invalidation_price;};
bool SF06_ValidateGoldenEvent(const SF06_GoldenExpectation &g,const SF06_AnatomyObservation &o,const SF01_AnatomyEvent &e,string &error){if(g.case_id==""){error="missing case id";return false;}if(o.observation_id!=g.expected_observation_id){error="observation id mismatch";return false;}if(e.event_id!=g.expected_event_id){error="event id mismatch";return false;}if(e.direction!=g.expected_direction){error="direction mismatch";return false;}if(MathAbs(e.reference_price-g.expected_reference_price)>1e-10){error="reference mismatch";return false;}if(MathAbs(e.invalidation_price-g.expected_invalidation_price)>1e-10){error="invalidation mismatch";return false;}error="";return true;}
#endif
