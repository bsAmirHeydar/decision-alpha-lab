#ifndef ALPHALAB_PORTFOLIO_MONITORING_MQH
#define ALPHALAB_PORTFOLIO_MONITORING_MQH
struct ALPortfolioTelemetry { int queue_count; int selected_count; int context_count; double reserved_risk; bool emergency_derisk; };
#endif
