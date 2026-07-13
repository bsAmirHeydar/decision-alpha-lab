#ifndef ALPHALAB_UCEI14_CONTRACTS
#define ALPHALAB_UCEI14_CONTRACTS
#include "UCEI14_Enums.mqh"
struct UCEI14BundleManifest{string bundle_hash;string preprocessing_hash;string model_hash;string export_hash;string policy_graph_hash;string rollback_hash;int generation;bool signature_valid;bool parity_pass;};
struct UCEI14Input{string request_id;string occurrence_id;string symbol;long known_time_ms;long received_at_ms;double score;string direction;double liquidity;bool blocked;bool kill_switch;};
struct UCEI14Vector{double values[5];};
struct UCEI14Output{double enter_long;double no_action;string label;};
struct UCEI14Decision{string request_id;string occurrence_id;string bundle_hash;int generation;UCEI14GateResult result;string label;string reason;bool order_authority;};
struct UCEI14Generation{string bundle_hash;string previous_hash;int generation;UCEI14GenerationState state;};
#endif
