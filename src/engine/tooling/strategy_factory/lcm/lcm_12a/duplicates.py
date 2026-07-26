from __future__ import annotations
from collections import defaultdict
import hashlib, re
from .canonical import digest_object, stable_id

def _rank(row):
    path = row["path"]
    rank = 50
    if path.startswith("docs/architecture/master/"): rank = 0
    elif path.startswith("docs/"): rank = 10
    elif "/docs/" in path: rank = 20
    elif "/fixtures/" in path: rank = 40
    elif path.startswith("registry/"): rank = 45
    return (rank, len(path.split("/")), len(path), path.lower())

def exact_groups(rows):
    by = defaultdict(list)
    for row in rows: by[row["byte_digest"]].append(row)
    groups=[]; membership={}
    for dig, members in sorted(by.items()):
        if len(members) < 2: continue
        members=sorted(members,key=_rank); canon=members[0]
        group={"duplicate_group_id":stable_id("DOCDUPBYTE",dig),"duplicate_type":"BYTE_DUPLICATE","evidence_digest":dig,"canonical_document_id":canon["document_id"],"canonical_path":canon["path"],"member_document_ids":[x["document_id"] for x in members],"member_paths":[x["path"] for x in members],"member_count":len(members),"proof":"IDENTICAL_SHA256_BYTES","validation_status":"PASS"}
        group["group_digest"]=digest_object(group,"group_digest");groups.append(group)
        for row in members: membership[row["document_id"]]=group
    return groups,membership

def normalized_groups(rows, exact_membership):
    by=defaultdict(list)
    for row in rows: by[row["normalized_digest"]].append(row)
    groups=[]; membership={}
    for dig,members in sorted(by.items()):
        byte_digests={x["byte_digest"] for x in members}
        if len(members)<2 or len(byte_digests)==1: continue
        members=sorted(members,key=_rank);canon=members[0]
        group={"duplicate_group_id":stable_id("DOCDUPNORM",dig),"duplicate_type":"NORMALIZED_DUPLICATE","evidence_digest":dig,"canonical_document_id":canon["document_id"],"canonical_path":canon["path"],"member_document_ids":[x["document_id"] for x in members],"member_paths":[x["path"] for x in members],"member_count":len(members),"normalization_contract":"LF_TRAILING_WS_DYNAMIC_FRONTMATTER_AND_SINGLE_BLANK_NORMALIZATION","proof":"IDENTICAL_NORMALIZED_SHA256","validation_status":"PASS"}
        group["group_digest"]=digest_object(group,"group_digest");groups.append(group)
        for row in members:
            if row["document_id"] not in exact_membership: membership[row["document_id"]]=group
    return groups,membership

def _content_lines(row):
    return {line.strip() for line in row["body"].splitlines() if len(line.strip()) >= 12 and not line.lstrip().startswith("#")}

def _tokens(row):
    return set(re.findall(r"[a-z0-9_]{3,}", row["body"].lower()))

def superset_and_overlap(rows):
    by=defaultdict(list)
    for row in rows: by[row["topic_key"]].append(row)
    supersets=[];overlaps=[]
    for key,members in sorted(by.items()):
        if len(members)<2: continue
        members=sorted(members,key=_rank)[:60]
        line_sets={x["document_id"]:_content_lines(x) for x in members}
        token_sets={x["document_id"]:_tokens(x) for x in members}
        pair_count=0
        for i,left in enumerate(members):
            for right in members[i+1:]:
                if pair_count>=120: break
                pair_count+=1
                if left["byte_digest"]==right["byte_digest"] or left["normalized_digest"]==right["normalized_digest"]: continue
                ls=line_sets[left["document_id"]];rs=line_sets[right["document_id"]]
                smaller,larger=(left,right) if len(ls)<=len(rs) else (right,left)
                ss=line_sets[smaller["document_id"]];ll=line_sets[larger["document_id"]]
                if len(ss)>=5 and ss.issubset(ll) and len(ll)>=len(ss)+2:
                    unique=sorted(ll-ss)
                    rec={"analysis_id":stable_id("DOCSUPERSET",smaller["document_id"],larger["document_id"]),"analysis_type":"PARTIAL_SUPERSET","topic_key":key,"subset_document_id":smaller["document_id"],"subset_path":smaller["path"],"superset_document_id":larger["document_id"],"superset_path":larger["path"],"shared_line_count":len(ss),"superset_unique_line_count":len(unique),"superset_unique_line_digests":["sha256:"+hashlib.sha256(x.encode()).hexdigest() for x in unique],"superset_unique_line_samples":unique[:20],"merge_or_removal_authorized":False,"validation_status":"PASS"}
                    rec["analysis_digest"]=digest_object(rec,"analysis_digest");supersets.append(rec);continue
                lt=token_sets[left["document_id"]];rt=token_sets[right["document_id"]]
                union=lt|rt
                score=(len(lt&rt)/len(union)) if union else 0.0
                if score>=0.72 and min(len(lt),len(rt))>=20:
                    rec={"analysis_id":stable_id("DOCOVERLAP",left["document_id"],right["document_id"]),"analysis_type":"SEMANTIC_OVERLAP_CANDIDATE","topic_key":key,"left_document_id":left["document_id"],"left_path":left["path"],"right_document_id":right["document_id"],"right_path":right["path"],"token_jaccard":round(score,6),"proof_ceiling":"LEXICAL_TOKEN_OVERLAP_NOT_SEMANTIC_EQUIVALENCE","owner_decision_required":True,"validation_status":"UNKNOWN"}
                    rec["analysis_digest"]=digest_object(rec,"analysis_digest");overlaps.append(rec)
            if pair_count>=120: break
    return supersets,overlaps
