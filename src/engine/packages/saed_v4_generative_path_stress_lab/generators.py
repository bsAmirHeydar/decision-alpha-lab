from __future__ import annotations
import random,math
from .contracts import GeneratorProgramContract
from .canonical import content_hash,stable_id
from .path_data import returns,spreads,liquidity,regimes
from .watermark import make
from .numerics import mean,std,clamp

def _seed(namespace,family,index,source_hash): return int(content_hash({'namespace':namespace,'family':family,'index':index,'source_hash':source_hash})[:16],16)
def _row(t,prev,ret,spread,vol,liq,regime,rng):
    close=max(1e-6,prev*(1+ret));open_=prev;wick=abs(ret)*0.35+abs(rng.gauss(0,max(abs(ret),1e-5)*0.15));high=max(open_,close)*(1+wick);low=min(open_,close)*(1-wick);half=max(1e-8,spread*close/2)
    return {'timestamp':int(t),'open':open_,'high':high,'low':max(1e-6,low),'close':close,'bid':max(1e-6,close-half),'ask':close+half,'volume':max(0.0,float(vol)),'liquidity':clamp(liq,0.0,1.0),'regime':str(regime)}
def _wrap(family,index,seed,context_id,start,step,rows,source_hash,member=0):
    gid=f'{family}::member::{member}';core={'path_id':stable_id('synthetic_path',{'family':family,'index':index,'seed':seed,'rows':rows}),'origin':'synthetic','generator_id':gid,'seed':seed,'context_id':context_id,'start_time':start,'step_seconds':step,'rows':rows,'research_only':True,'stress_labels':[],'source_hash':source_hash}
    core['watermark']=make(gid,seed,source_hash);return core

def _pool(real_paths):
    return {'returns':[x for p in real_paths for x in returns(p)],'spreads':[x for p in real_paths for x in spreads(p)],'liquidity':[x for p in real_paths for x in liquidity(p)],'regimes':[x for p in real_paths for x in regimes(p)]}
def _transition_model(real_paths):
    regs=sorted({x for p in real_paths for x in regimes(p)});counts={a:{b:1.0 for b in regs} for a in regs};stats={g:[] for g in regs}
    for p in real_paths:
        rr=returns(p);gg=regimes(p)
        for i,r in enumerate(rr):stats[gg[i+1]].append(r)
        for a,b in zip(gg[:-1],gg[1:]):counts[a][b]+=1
    probs={a:[counts[a][b]/sum(counts[a].values()) for b in regs] for a in regs}
    return regs,probs,{g:(mean(stats[g]),max(std(stats[g]),1e-5)) for g in regs}
def _choice_weighted(rng,items,weights):
    x=rng.random();s=0
    for item,w in zip(items,weights):
        s+=w
        if x<=s:return item
    return items[-1]

def generate_family(family,index,real_paths,program_mapping,source_hash,member=0):
    p=GeneratorProgramContract.from_mapping(program_mapping);seed=_seed(p.seed_namespace,family,index+member*10000,source_hash);rng=random.Random(seed);base=real_paths[index%len(real_paths)];start=int(base['start_time'])+1000000+(index+member*100)*p.horizon*int(base['step_seconds']);step=int(base['step_seconds']);prev=float(base['rows'][-1]['close']);pool=_pool(real_paths);rows=[]
    if family=='moving_block_bootstrap':
        source=random.Random(seed+17).choice(real_paths);rr=returns(source);ss=spreads(source);ll=liquidity(source);gg=regimes(source);seq=[]
        while len(seq)<p.horizon:
            st=rng.randrange(0,max(1,len(rr)-p.block_length+1));seq.extend(range(st,min(len(rr),st+p.block_length)))
        for k,ix in enumerate(seq[:p.horizon]):
            rows.append(_row(start+k*step,prev,rr[ix],ss[min(ix+1,len(ss)-1)],100+20*rng.random(),ll[min(ix+1,len(ll)-1)],gg[min(ix+1,len(gg)-1)],rng));prev=rows[-1]['close']
    elif family=='regime_markov':
        regs,probs,stats=_transition_model(real_paths);g=regs[index%len(regs)]
        for k in range(p.horizon):
            g=_choice_weighted(rng,regs,probs[g]);mu,sd=stats[g];ret=max(-0.15,min(0.15,rng.gauss(mu,sd)));spr=max(1e-5,rng.choice(pool['spreads']));liq=clamp(rng.choice(pool['liquidity'])+rng.gauss(0,0.03))
            rows.append(_row(start+k*step,prev,ret,spr,100+35*rng.random(),liq,g,rng));prev=rows[-1]['close']
    elif family=='latent_linear_ensemble':
        rs=pool['returns'];mu=mean(rs);sd=max(std(rs),1e-5);phi=max(-0.75,min(0.75,0.2+0.08*(member-(p.ensemble_members-1)/2)));latent=0.0;g=pool['regimes'][index%len(pool['regimes'])]
        for k in range(p.horizon):
            latent=phi*latent+rng.gauss(0,sd)*(1+0.05*member);ret=max(-0.15,min(0.15,mu+latent));spr=max(1e-5,mean(pool['spreads'])*(1+abs(latent)*20));liq=clamp(mean(pool['liquidity'])-abs(latent)*4+rng.gauss(0,0.02));g='volatile' if abs(ret)>1.4*sd else ('trend' if abs(latent)>0.6*sd else 'range')
            rows.append(_row(start+k*step,prev,ret,spr,95+30*rng.random(),liq,g,rng));prev=rows[-1]['close']
    elif family=='residual_flow_reference':
        rs=sorted(pool['returns']);sd=max(std(rs),1e-5);state=0.0
        for k in range(p.horizon):
            q=(rng.random()+rng.random()+rng.random())/3;ix=min(len(rs)-1,int(q*len(rs)));innovation=rs[ix];state=0.35*state+0.65*innovation+rng.gauss(0,0.15*sd);ret=max(-0.15,min(0.15,state));spr=max(1e-5,rng.choice(pool['spreads'])*(1+0.3*abs(ret)/sd));liq=clamp(rng.choice(pool['liquidity'])-0.08*abs(ret)/sd);g='tail' if abs(ret)>2*sd else ('trend' if state*innovation>0 else 'range')
            rows.append(_row(start+k*step,prev,ret,spr,90+40*rng.random(),liq,g,rng));prev=rows[-1]['close']
    else: raise ValueError('unknown generator family')
    return _wrap(family,index,seed,base['context_id'],start,step,rows,source_hash,member)
def generate_registry(real_paths,program_mapping,source_hash,ledger=None):
    p=GeneratorProgramContract.from_mapping(program_mapping);paths=[];registry=[]
    for family in p.families:
        members=p.ensemble_members if family=='latent_linear_ensemble' else 1
        for member in range(members):
            gid=f'{family}::member::{member}';registry.append({'generator_id':gid,'family':family,'member':member,'deterministic':True,'action_masked':True,'synthetic_only':True})
            if ledger:ledger.consume('generator_trials',1)
            for i in range(p.paths_per_family):
                paths.append(generate_family(family,i,real_paths,program_mapping,source_hash,member));
                if ledger:ledger.consume('generated_paths',1)
    out={'registry':registry,'generator_count':len(registry),'paths':paths,'path_count':len(paths),'source_hash':source_hash,'research_only':True};out['generator_registry_hash']=content_hash({'registry':registry,'source_hash':source_hash});out['rollout_set_hash']=content_hash(paths);return out
