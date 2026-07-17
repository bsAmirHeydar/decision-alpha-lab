#ifndef SAED_V4_29_SUBMISSION_MQH
#define SAED_V4_29_SUBMISSION_MQH
#include "SAEDV429Types.mqh"
bool SAEDV429SubmissionFrozen(const SAEDV429Commitment &c){ return c.frozen && c.submitted_at>0; }
#endif
