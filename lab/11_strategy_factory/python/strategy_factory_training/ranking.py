from __future__ import annotations
from dataclasses import dataclass
from .models import DatasetRow
from .hashing import stable_id

@dataclass(frozen=True,slots=True)
class RankingPair:
    fold_id:str; role:int; preferred_row_id:str; other_row_id:str; utility_gap:float; pair_id:str

def build_ranking_pairs(rows,max_pairs:int=100000,minimum_gap:float=0.0)->tuple[RankingPair,...]:
    labeled=[row for row in rows if row.label_available]
    pairs=[]
    for i,left in enumerate(labeled):
        for right in labeled[i+1:]:
            if left.fold_id!=right.fold_id or left.role!=right.role:continue
            gap=float(left.label_value-right.label_value)
            if abs(gap)<=minimum_gap:continue
            preferred,other=(left,right) if gap>0 else (right,left)
            canonical=f"{preferred.fold_id}|{int(preferred.role)}|{preferred.row_id}|{other.row_id}|{abs(gap):.17g}"
            pairs.append(RankingPair(preferred.fold_id,int(preferred.role),preferred.row_id,other.row_id,abs(gap),stable_id("rpair",canonical)))
            if len(pairs)>max_pairs:raise ValueError("ranking pair bound exceeded")
    return tuple(sorted(pairs,key=lambda p:p.pair_id))

def pairwise_accuracy(pairs,scores:dict[str,float])->float:
    if not pairs:raise ValueError("empty ranking pair set")
    return sum(scores[p.preferred_row_id]>scores[p.other_row_id] for p in pairs)/len(pairs)
