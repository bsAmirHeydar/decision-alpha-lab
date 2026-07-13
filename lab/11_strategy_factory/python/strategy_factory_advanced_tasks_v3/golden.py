from strategy_factory_trainers_v3.contracts import TrainingRow
from strategy_factory_trainers_v3.enums import SplitRole
from .contracts import LoggedPolicyRow,SurvivalObservation,ActionMask
from .canonical import canonical_sha256,stable_id

def ranking_rows():
 rows=[]
 for g in range(4):
  for i in range(5):
   x=(float(i),float(g),float(i*g));u=1.7*i-.2*g+.05*i*g;rows.append(TrainingRow(f'rank_{g}_{i}',x,(u,),SplitRole.TRAIN,'f0',f'c{g}',1000*g+i,1000*g+i,1.,f'g{g}'))
 return tuple(rows)
def treatment_rows():
 rows=[];actions=('wide_stop','tight_stop','trail_runner')
 for i in range(90):
  a=actions[i%3];x=(float(i%7),float((i//7)%5),float(i%2));bonus={'wide_stop':.4,'tight_stop':.8,'trail_runner':1.1}[a];u=bonus+.08*x[0]-.03*x[1]+(.2 if a=='trail_runner' and x[2] else 0);rows.append(TrainingRow(f'treat_{i}',x,(u,),SplitRole.TRAIN,'f0',f'c{i//3}',i,i,1.,'',a))
 return tuple(rows),actions
def survival_observations():
 return tuple(SurvivalObservation(f'surv_{i}',(i%6+1)*60000,1 if i%4 else 0,1 if i%3 else 2,1.,i) for i in range(36))
def quantile_values():return tuple(-2.5+.1*i+(1 if i%7==0 else 0) for i in range(60))
def policy_rows():
 actions=('wide_stop','tight_stop','trail_runner');rows=[]
 for i in range(90):
  a=actions[i%3];reward={'wide_stop':.35,'tight_stop':.55,'trail_runner':.75}[a]+.01*(i%5);rows.append(LoggedPolicyRow(f'pol_{i}',(float(i%5),float(i%2)),a,reward,1/3,actions,f'c{i//3}',i))
 return tuple(rows),actions
def mask(row_id,actions):
 h=canonical_sha256({'row':row_id,'a':actions});return ActionMask(stable_id('ucemask',h),row_id,tuple(actions),{},0,h)
