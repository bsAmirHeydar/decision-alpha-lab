#ifndef FP_SAEDV430EXCHANGE_MQH
#define FP_SAEDV430EXCHANGE_MQH
struct FP_SAEDV430ExchangeReceipt { string receipt_id; string assignment_id; string receiver_lab_id; string package_hash; bool network_egress; bool payload_mutated; bool delivered; };
#endif
