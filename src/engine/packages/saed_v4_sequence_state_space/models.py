from __future__ import annotations
from dataclasses import dataclass
from typing import Any
from .canonical import content_hash
from .initialization import matrix,vector
from .numerics import tanh,sigmoid,softplus,dot,matvec,mean_vec
from .errors import ContractError

@dataclass
class ModelState:
    hidden:tuple[float,...]
    history:tuple[tuple[float,...],...]=()
    step_count:int=0

class BaseModel:
    architecture='base'
    def __init__(self,candidate_id,input_dim,state_dim,seed,window=4):
        self.candidate_id=candidate_id;self.input_dim=input_dim;self.state_dim=state_dim;self.seed=seed;self.window=window
    def initial_state(self):return ModelState(tuple(0.0 for _ in range(self.state_dim)),(),0)
    def step(self,x,state,dt_seconds=1.0):raise NotImplementedError
    def batch(self,xs,dts=None,state=None):
        state=state or self.initial_state();outs=[];dts=dts or [1.0]*len(xs)
        for x,dt in zip(xs,dts):
            y,state=self.step(tuple(map(float,x)),state,float(dt));outs.append(y)
        return tuple(outs),state
    def spec(self):
        m={'candidate_id':self.candidate_id,'architecture':self.architecture,'input_dim':self.input_dim,'state_dim':self.state_dim,'seed':self.seed,'window':self.window}
        return {**m,'model_spec_hash':content_hash(m)}

class EMARecurrentModel(BaseModel):
    architecture='ema_recurrent'
    def __init__(self,*a,**k):
        super().__init__(*a,**k);self.b=matrix(f'{self.candidate_id}:b',self.state_dim,self.input_dim,0.12);self.bias=vector(f'{self.candidate_id}:bias',self.state_dim,0.02);self.decay=tuple(0.65+0.25*sigmoid(v) for v in vector(f'{self.candidate_id}:decay',self.state_dim,1.0))
    def step(self,x,state,dt_seconds=1.0):
        if len(x)!=self.input_dim:raise ContractError('input width mismatch')
        proj=matvec(self.b,x);h=tuple(tanh((self.decay[i]**max(1.0,dt_seconds/60.0))*state.hidden[i]+proj[i]+self.bias[i]) for i in range(self.state_dim));return h,ModelState(h,(),state.step_count+1)

class CausalConvolutionModel(BaseModel):
    architecture='causal_convolution'
    def __init__(self,*a,**k):super().__init__(*a,**k);self.w=matrix(f'{self.candidate_id}:w',self.state_dim,self.input_dim,0.11);self.mix=vector(f'{self.candidate_id}:mix',self.window,0.5)
    def step(self,x,state,dt_seconds=1.0):
        hist=(state.history+(tuple(x),))[-self.window:];weights=[abs(self.mix[-len(hist)+i])+0.05 for i in range(len(hist))];z=tuple(sum(weights[i]*hist[i][j] for i in range(len(hist)))/sum(weights) for j in range(self.input_dim));h=tuple(tanh(v) for v in matvec(self.w,z));return h,ModelState(h,hist,state.step_count+1)

class DiagonalSSMModel(BaseModel):
    architecture='diagonal_ssm'
    def __init__(self,*a,**k):super().__init__(*a,**k);self.b=matrix(f'{self.candidate_id}:b',self.state_dim,self.input_dim,0.10);self.rate=tuple(0.01+softplus(v)*0.03 for v in vector(f'{self.candidate_id}:rate',self.state_dim,0.8));self.skip=matrix(f'{self.candidate_id}:skip',self.state_dim,self.input_dim,0.03)
    def step(self,x,state,dt_seconds=1.0):
        import math
        u=matvec(self.b,x);skip=matvec(self.skip,x);dt=max(0.001,min(3600.0,float(dt_seconds)))
        h=tuple(tanh(math.exp(-self.rate[i]*dt/60.0)*state.hidden[i]+(1.0-math.exp(-self.rate[i]*dt/60.0))*u[i]+skip[i]) for i in range(self.state_dim));return h,ModelState(h,(),state.step_count+1)

class SelectiveSSMModel(DiagonalSSMModel):
    architecture='selective_ssm'
    def __init__(self,*a,**k):super().__init__(*a,**k);self.g=matrix(f'{self.candidate_id}:gate',self.state_dim,self.input_dim,0.15)
    def step(self,x,state,dt_seconds=1.0):
        import math
        u=matvec(self.b,x);g=tuple(sigmoid(v) for v in matvec(self.g,x));dt=max(0.001,min(3600.0,float(dt_seconds)))
        h=[]
        for i in range(self.state_dim):
            decay=math.exp(-self.rate[i]*dt/60.0*(0.25+g[i]));candidate=tanh(decay*state.hidden[i]+(1-decay)*u[i]);h.append(g[i]*candidate+(1-g[i])*state.hidden[i])
        h=tuple(h);return h,ModelState(h,(),state.step_count+1)

class LocalCausalAttentionModel(BaseModel):
    architecture='local_causal_attention'
    def __init__(self,*a,**k):
        super().__init__(*a,**k);self.q=matrix(f'{self.candidate_id}:q',self.state_dim,self.input_dim,0.10);self.k=matrix(f'{self.candidate_id}:k',self.state_dim,self.input_dim,0.10);self.v=matrix(f'{self.candidate_id}:v',self.state_dim,self.input_dim,0.10)
    def step(self,x,state,dt_seconds=1.0):
        import math
        hist=(state.history+(tuple(x),))[-self.window:];q=matvec(self.q,x);keys=[matvec(self.k,r) for r in hist];vals=[matvec(self.v,r) for r in hist];scores=[dot(q,k)/(self.state_dim**0.5) for k in keys];mx=max(scores);ex=[math.exp(max(-40,min(40,s-mx))) for s in scores];den=sum(ex);h=tuple(tanh(sum(ex[i]*vals[i][j] for i in range(len(vals)))/den) for j in range(self.state_dim));return h,ModelState(h,hist,state.step_count+1)

class HybridSSMAttentionModel(BaseModel):
    architecture='hybrid_ssm_attention'
    def __init__(self,*a,**k):
        super().__init__(*a,**k);self.ssm=SelectiveSSMModel(self.candidate_id+':ssm',self.input_dim,self.state_dim,self.seed,self.window);self.attn=LocalCausalAttentionModel(self.candidate_id+':attn',self.input_dim,self.state_dim,self.seed,self.window)
    def initial_state(self):return ModelState(tuple(0.0 for _ in range(self.state_dim)),(),0)
    def step(self,x,state,dt_seconds=1.0):
        # The hybrid state serializes both component states in a deterministic concatenated history convention.
        ssm_hidden=state.hidden[:self.state_dim] if len(state.hidden)>=self.state_dim else tuple(0.0 for _ in range(self.state_dim));ss=ModelState(tuple(ssm_hidden),(),state.step_count)
        ah=state.history
        astate=ModelState(tuple(0.0 for _ in range(self.state_dim)),ah,state.step_count)
        ys,ns=self.ssm.step(x,ss,dt_seconds);ya,na=self.attn.step(x,astate,dt_seconds);h=tuple(tanh(0.62*ys[i]+0.38*ya[i]) for i in range(self.state_dim));return h,ModelState(h,na.history,state.step_count+1)

def build_model(spec,input_dim):
    cls={'ema_recurrent':EMARecurrentModel,'causal_convolution':CausalConvolutionModel,'diagonal_ssm':DiagonalSSMModel,'selective_ssm':SelectiveSSMModel,'local_causal_attention':LocalCausalAttentionModel,'hybrid_ssm_attention':HybridSSMAttentionModel}[spec.architecture]
    return cls(spec.candidate_id,input_dim,spec.state_dim,spec.seed,min(8,spec.context_steps))
