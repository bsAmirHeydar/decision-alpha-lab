from __future__ import annotations
from collections import defaultdict
from .canonical import normalize_text,seal,content_hash
from .contracts import require_exact,require_list,require_unique,require_int
from .errors import RetrievalError

def build_index(memory:dict,negative:dict)->dict:
    postings=defaultdict(list); neg={x["memory_id"] for x in negative["records"]}
    for x in memory["entries"]:
        tokens=sorted(set(normalize_text(" ".join([x["title"],x["statement"]," ".join(x["tags"])] )).split()))
        for t in tokens: postings[t].append(x["memory_id"])
    rows=[{"token":t,"memory_ids":sorted(ids),"document_frequency":len(set(ids))} for t,ids in sorted(postings.items())]
    return seal({"phase":"SAED_V4_36","postings":rows,"token_count":len(rows),"negative_memory_ids":sorted(neg),"deterministic":True,"embedding_service_used":False,"network_access":False,"research_only":True},"v436_index","index_id","index_hash")

def retrieve(index:dict,memory:dict,queries:list[dict])->dict:
    queries=require_list(queries,"queries",3); require_unique(queries,"query_id","queries"); by={x["memory_id"]:x for x in memory["entries"]}; post={x["token"]:set(x["memory_ids"]) for x in index["postings"]}; rows=[]
    for q in queries:
        require_exact(q,["query_id","text","required_kinds","required_tags","include_negative","top_k"]); require_int(q["top_k"],"top_k",1,50)
        tokens=sorted(set(normalize_text(q["text"]).split())); scores=defaultdict(float)
        for t in tokens:
            for mid in post.get(t,set()): scores[mid]+=1.0
        results=[]
        for mid,score in scores.items():
            x=by[mid]
            if q["required_kinds"] and x["kind"] not in q["required_kinds"]: continue
            if q["required_tags"] and not set(q["required_tags"])<=set(x["tags"]): continue
            isneg=mid in set(index["negative_memory_ids"])
            if isneg and not q["include_negative"]: continue
            results.append({"memory_id":mid,"score":round(score/max(1,len(tokens)),8),"negative_knowledge":isneg,"kind":x["kind"],"title":x["title"]})
        results=sorted(results,key=lambda x:(-x["score"],not x["negative_knowledge"],x["memory_id"]))[:q["top_k"]]
        rows.append({"query_id":q["query_id"],"query_hash":content_hash(q),"results":results,"result_count":len(results),"negative_recall_count":sum(x["negative_knowledge"] for x in results)})
    return seal({"phase":"SAED_V4_36","queries":rows,"query_count":len(rows),"deterministic":True,"research_only":True},"v436_retrieval","receipt_id","receipt_hash")
