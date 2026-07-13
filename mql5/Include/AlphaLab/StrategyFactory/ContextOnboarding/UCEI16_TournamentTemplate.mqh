#ifndef ALPHALAB_UCEI16_TOURNAMENT_TEMPLATE_MQH
#define ALPHALAB_UCEI16_TOURNAMENT_TEMPLATE_MQH
struct UCEI16_TournamentTemplate { string template_id; string context_spec_hash; int seed; bool final_test_sealed; bool fixture_not_alpha_proof; int stage_count; };
bool UCEI16_ValidateTournamentTemplate(const UCEI16_TournamentTemplate &t){ return StringLen(t.template_id)>0 && StringLen(t.context_spec_hash)==64 && t.seed>=0 && t.final_test_sealed && t.fixture_not_alpha_proof && t.stage_count==9; }
#endif
