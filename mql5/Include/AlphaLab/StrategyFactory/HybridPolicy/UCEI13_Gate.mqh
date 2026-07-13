#ifndef ALPHALAB_UCEI13_GATE
#define ALPHALAB_UCEI13_GATE
#include "UCEI13_Authority.mqh"
#include "UCEI13_Fallback.mqh"
bool UCEI13ModelUsable(const bool signed_promote,const bool stale,const bool ood,const bool low_confidence,const bool missing_view){return signed_promote&&!stale&&!ood&&!low_confidence&&!missing_view;}
UCEI13Decision UCEI13Resolve(const UCEI13ManualDecision &manual,const UCEI13ModelOutput &model,const bool signed_promote,const bool kill_switch,const bool risk_rejected,const bool operator_veto){UCEI13Decision d;d.authority=UCEI13ResolveAuthority(kill_switch,risk_rejected,manual.vetoed,operator_veto);if(d.authority==UCEI13_KILL||d.authority==UCEI13_RISK||d.authority==UCEI13_OPERATOR||d.authority==UCEI13_MANUAL){d.status=UCEI13_REJECTED;d.fallback=UCEI13_REJECT;d.action="reject";return d;}if(!UCEI13ModelUsable(signed_promote,model.stale,model.ood,model.low_confidence,model.missing_view)){d.status=manual.eligible?UCEI13_APPROVED:UCEI13_INELIGIBLE;d.authority=UCEI13_MANUAL;d.fallback=UCEI13_MANUAL_ONLY;d.action=manual.action;d.treatment=manual.treatment;d.risk_tier=manual.risk_tier;return d;}d.status=UCEI13_APPROVED;d.authority=UCEI13_MODEL;d.action=model.action;d.treatment=model.treatment;d.risk_tier=model.risk_tier;return d;}
#endif
