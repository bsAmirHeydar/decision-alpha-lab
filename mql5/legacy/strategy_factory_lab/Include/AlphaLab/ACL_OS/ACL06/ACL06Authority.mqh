#ifndef ALPHALAB_ACL06_AUTHORITY_MQH
#define ALPHALAB_ACL06_AUTHORITY_MQH
struct ACL06AuthorityBoundary { bool network_allowed; bool secret_allowed; bool order_allowed; bool capital_allowed; };
bool ACL06AuthorityIsSafe(const ACL06AuthorityBoundary &x){ return !x.network_allowed && !x.secret_allowed && !x.order_allowed && !x.capital_allowed; }
#endif
