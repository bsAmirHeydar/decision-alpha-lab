#pragma once
struct ACL13AuthorityGuard { bool network_allowed; bool pilot_execution_allowed; bool runtime_activation_allowed; bool live_order_allowed; bool capital_allowed; };
bool ACL13AuthorityClosed(const ACL13AuthorityGuard &g){ return !g.network_allowed && !g.pilot_execution_allowed && !g.runtime_activation_allowed && !g.live_order_allowed && !g.capital_allowed; }
