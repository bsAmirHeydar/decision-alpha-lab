def test_categories(load):
 c=load("deletion_candidate_ledger.json")["category_counts"];assert c["QUARANTINED_DOCUMENTATION_REDIRECT"]==136 and c["EXACT_DUPLICATE_DOCUMENTATION"]==976 and sum(v for k,v in c.items() if k.startswith("ROOT_"))==1069
