from __future__ import annotations
from .contracts import FoldSpec
from .errors import TournamentError

def build_walk_forward_folds(start_ms:int,end_ms:int,fold_count:int=3,embargo_ms:int=1,purge_ms:int=1)->tuple[FoldSpec,...]:
 if fold_count<1:raise TournamentError('invalid_fold_count','fold count positive')
 span=end_ms-start_ms
 if span<fold_count*4:raise TournamentError('insufficient_time_span','time span too small')
 step=span//(fold_count+3);out=[]
 for i in range(fold_count):
  train_start=start_ms;train_end=start_ms+step*(i+1);val_end=train_end+step;test_end=val_end+step
  if test_end>end_ms:test_end=end_ms
  out.append(FoldSpec(f'fold_{i:03d}',train_start,train_end,val_end,test_end,embargo_ms,purge_ms))
 return tuple(out)

def assert_no_overlap(folds:tuple[FoldSpec,...]):
 for f in folds:
  if f.train_end_ms+f.purge_ms>=f.validation_end_ms:raise TournamentError('purge_overlap','purge overlaps validation')
  if f.validation_end_ms+f.embargo_ms>=f.test_end_ms:raise TournamentError('embargo_overlap','embargo overlaps test')
 return True
