from math import log2
from .contracts import RankingPair,RankingMetricReport
from .canonical import stable_id,canonical_sha256
from .errors import RankingError
from .math_utils import dot,sigmoid

def validate_groups(rows):
 groups={}
 for row in rows:
  if not row.ranking_group:raise RankingError('ranking_group_required','ranking row lacks ranking_group',{'row_id':row.row_id})
  groups.setdefault(row.ranking_group,[]).append(row)
 if not groups:raise RankingError('empty_ranking_dataset','no ranking rows')
 return groups

def build_pairs(rows,max_pairs_per_group=4096,min_gap=0.0):
 pairs=[]
 for gid,items in sorted(validate_groups(rows).items()):
  ordered=sorted(items,key=lambda r:r.row_id)
  count=0
  for i in range(len(ordered)):
   for j in range(i+1,len(ordered)):
    a,b=ordered[i],ordered[j];gap=float(a.target[0]-b.target[0])
    if abs(gap)<=min_gap:continue
    hi,lo=(a,b) if gap>0 else (b,a);weight=max(1e-12,(hi.sample_weight+lo.sample_weight)*0.5*abs(gap))
    material={'g':gid,'hi':hi.row_id,'lo':lo.row_id,'w':weight};pairs.append(RankingPair(stable_id('ucerankpair',material),gid,hi.row_id,lo.row_id,weight,abs(gap)));count+=1
    if count>=max_pairs_per_group:break
   if count>=max_pairs_per_group:break
 return tuple(pairs)

class PairwiseLinearRanker:
 def __init__(self,epochs=240,learning_rate=.04,l2=.001,max_pairs_per_group=4096):self.epochs=epochs;self.learning_rate=learning_rate;self.l2=l2;self.max_pairs_per_group=max_pairs_per_group;self.coefficients=();self.feature_order=();self.state_hash=''
 def fit(self,rows,feature_order):
  by={r.row_id:r for r in rows};pairs=build_pairs(rows,self.max_pairs_per_group)
  if not pairs:raise RankingError('no_comparable_pairs','ranking dataset has no utility differences')
  p=len(feature_order);coef=[0.]*p;den=sum(x.weight for x in pairs) or 1.
  for _ in range(self.epochs):
   grad=[0.]*p
   for pair in pairs:
    hi,lo=by[pair.preferred_row_id],by[pair.other_row_id];d=[a-b for a,b in zip(hi.features,lo.features)];err=sigmoid(-dot(coef,d))*pair.weight
    for j in range(p):grad[j]-=err*d[j]
   for j in range(p):coef[j]-=self.learning_rate*(grad[j]/den+self.l2*coef[j])
  self.coefficients=tuple(coef);self.feature_order=tuple(feature_order);self.state_hash=canonical_sha256({'coef':coef,'features':feature_order,'pairs':[p.pair_id for p in pairs]});return self
 def score(self,features):return dot(self.coefficients,features)
 def predict(self,rows):return {r.row_id:self.score(r.features) for r in rows}

def _dcg(relevances):return sum((2**max(-20.,min(20.,r))-1)/log2(i+2) for i,r in enumerate(relevances))
def ranking_metrics(rows,scores,k=3):
 groups=validate_groups(rows);pair_ok=pair_total=ndcg=mapv=topu=0.;weights=[]
 for gid,items in sorted(groups.items()):
  ordered=sorted(items,key=lambda r:(-scores[r.row_id],r.row_id));ideal=sorted(items,key=lambda r:(-r.target[0],r.row_id));kk=min(k,len(items));rel=[r.target[0] for r in ordered[:kk]];irel=[r.target[0] for r in ideal[:kk]];idcg=_dcg(irel);ndcg+=_dcg(rel)/idcg if idcg else 1.
  positive_cut=sum(1 for r in items if r.target[0]>0);hits=0;ap=0.
  for i,r in enumerate(ordered[:kk],1):
   if r.target[0]>0:hits+=1;ap+=hits/i
  mapv+=ap/max(1,min(positive_cut,kk));topu+=sum(r.target[0]*r.sample_weight for r in ordered[:kk])/max(1e-12,sum(r.sample_weight for r in ordered[:kk]));weights.append((gid,sum(r.sample_weight for r in items)))
  for i in range(len(items)):
   for j in range(i+1,len(items)):
    a,b=items[i],items[j]
    if a.target[0]==b.target[0]:continue
    ww=(a.sample_weight+b.sample_weight)/2;pair_total+=ww;pair_ok+=ww*(((scores[a.row_id]-scores[b.row_id])*(a.target[0]-b.target[0]))>0)
 n=len(groups);evidence={'groups':weights,'scores':scores,'k':k};h=canonical_sha256(evidence)
 return RankingMetricReport(stable_id('ucerankreport',h),n,len(rows),int(pair_total),pair_ok/pair_total if pair_total else .5,ndcg/n,mapv/n,topu/n,k,canonical_sha256(weights),h)
