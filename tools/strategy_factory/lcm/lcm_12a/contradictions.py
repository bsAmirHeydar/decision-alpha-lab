from __future__ import annotations
from collections import defaultdict
import re
from .canonical import digest_object, stable_id

_MODAL=re.compile(r"\b(must|shall|required|cannot|must not|shall not|forbidden|never|allowed|may|should|should not)\b",re.I)
_NEGATIVE={"cannot","must not","shall not","forbidden","never","should not"}

def _clauses(row):
    out=[]
    for number,line in enumerate(row["body"].splitlines(),1):
        line=line.strip()
        if len(line)<20 or len(line)>500:continue
        match=_MODAL.search(line)
        if not match:continue
        modal=match.group(1).lower();polarity="NEGATIVE" if modal in _NEGATIVE else "POSITIVE"
        normalized=_MODAL.sub(" ",line.lower())
        tokens=set(re.findall(r"[a-z0-9_]{3,}",normalized))-{ "the","and","that","this","with","from","into","only","must","shall","should","allowed","required"}
        if len(tokens)>=3:out.append((number,line,polarity,tokens))
    return out

def detect_contradictions(rows):
    by=defaultdict(list)
    for row in rows:by[row["topic_key"]].append(row)
    records=[]
    for topic,members in sorted(by.items()):
        if len(members)<2:continue
        clauses={row["document_id"]:_clauses(row)[:120] for row in members[:40]}
        count=0
        for i,left in enumerate(members[:40]):
            for right in members[i+1:40]:
                if count>=80:break
                for ln,lline,lpol,lt in clauses[left["document_id"]]:
                    for rn,rline,rpol,rt in clauses[right["document_id"]]:
                        if lpol==rpol:continue
                        union=lt|rt;score=len(lt&rt)/len(union) if union else 0
                        if score<0.62:continue
                        rec={"contradiction_id":stable_id("DOCCONFLICT",left["document_id"],right["document_id"],ln,rn),"topic_key":topic,"left_document_id":left["document_id"],"left_path":left["path"],"left_line":ln,"left_clause":lline,"left_polarity":lpol,"right_document_id":right["document_id"],"right_path":right["path"],"right_line":rn,"right_clause":rline,"right_polarity":rpol,"lexical_alignment":round(score,6),"decision_status":"BLOCKED_OWNER_DECISION","silent_harmonization_performed":False,"validation_status":"UNKNOWN"}
                        rec["contradiction_digest"]=digest_object(rec,"contradiction_digest");records.append(rec);count+=1;break
                    if count>=80:break
                if count>=80:break
            if count>=80:break
    unique={r["contradiction_id"]:r for r in records}
    return sorted(unique.values(),key=lambda x:(x["topic_key"],x["left_path"],x["right_path"],x["left_line"],x["right_line"]))
