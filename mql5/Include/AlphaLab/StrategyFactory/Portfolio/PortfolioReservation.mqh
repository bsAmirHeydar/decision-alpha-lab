#ifndef ALPHALAB_PORTFOLIO_RESERVATION_MQH
#define ALPHALAB_PORTFOLIO_RESERVATION_MQH
struct ALPortfolioReservation { string reservation_id; string candidate_id; double risk; int state; long expires_at_ms; string previous_hash; string entry_hash; };
#endif
