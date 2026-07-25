#pragma once
bool ACL13ClaimsClosed(const bool validation_claim,const bool alpha_claim,const bool live_order,const bool capital){ return !validation_claim && !alpha_claim && !live_order && !capital; }
