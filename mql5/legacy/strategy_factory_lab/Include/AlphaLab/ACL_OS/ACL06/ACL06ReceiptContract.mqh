#ifndef ALPHALAB_ACL06_RECEIPT_CONTRACT_MQH
#define ALPHALAB_ACL06_RECEIPT_CONTRACT_MQH
struct ACL06TaskReceipt { string task_id; string task_receipt_digest; string output_blob_digest; int attempt; bool success; };
#endif
