#ifndef ALPHALAB_UCEI16_DIFFERENTIAL_MQH
#define ALPHALAB_UCEI16_DIFFERENTIAL_MQH
struct UCEI16_DifferentialObservation { string observation_id; long known_time_ms; double legacy_value; double canonical_value; double delta; bool matched; };
double UCEI16_AbsoluteDelta(const double a,const double b){ return MathAbs(a-b); }
bool UCEI16_Matches(const double a,const double b,const double tolerance){ return UCEI16_AbsoluteDelta(a,b)<=tolerance; }
#endif
