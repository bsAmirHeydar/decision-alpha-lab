from __future__ import annotations
from collections import Counter
def summarize(inventory:list[dict],families:dict,variants:list[dict],embedded:list[dict],unknowns:list[dict])->dict:
    return {"setup_identity_count":len(inventory),"family_count":families["family_count"],"variant_count":len(variants),"embedded_setup_candidate_count":len(embedded),"open_unknown_count":len(unknowns),"contract_status_counts":dict(Counter(x["contract_status"] for x in inventory)),"implementation_authorized_setup_count":sum(x["implementation_authorized"] for x in inventory)}
