from __future__ import annotations
import copy,math
from .contracts import StressProgramContract
from .canonical import content_hash,stable_id
from .watermark import make
from .numerics import clamp

def apply_stress(path,family,severity,index=0):
    q=copy.deepcopy(path);rows=q['rows'];original=copy.deepcopy(path['rows']);n=len(rows);pivot=max(1,min(n-2,int((0.25+0.5*((index%7)/6))*n)));sev=float(severity)
    for i,r in enumerate(rows):
        prev=rows[i-1]['close'] if i else r['open']
        base_prev=original[i-1]['close'] if i else original[i]['open']
        ret=original[i]['close']/base_prev-1 if base_prev else 0.0
        if family=='gap_down' and i>=pivot: factor=1-0.08*sev
        elif family=='gap_up' and i>=pivot: factor=1+0.08*sev
        else: factor=1.0
        if factor!=1.0:
            for k in ['open','high','low','close','bid','ask']:r[k]=max(1e-6,float(r[k])*factor)
        if family=='volatility_burst' and pivot<=i<pivot+max(2,n//5):
            mult=1+3.5*sev;new_close=max(1e-6,float(prev)*(1+ret*mult));r['open']=float(prev);r['close']=new_close;r['high']=max(r['open'],new_close)*(1+abs(ret)*mult*0.35);r['low']=max(1e-6,min(r['open'],new_close)*(1-abs(ret)*mult*0.35));mid=new_close;half=max(1e-8,(r['ask']-r['bid'])*mult/2);r['bid']=mid-half;r['ask']=mid+half;r['regime']='volatile_stress'
        elif family=='liquidity_collapse' and i>=pivot:r['liquidity']=clamp(float(r['liquidity'])*(1-0.85*sev));r['volume']=max(0.0,float(r['volume'])*(1-0.65*sev));r['regime']='liquidity_stress'
        elif family=='spread_blowout' and i>=pivot:
            mid=float(r['close']);half=(float(r['ask'])-float(r['bid']))*(1+6*sev)/2;r['bid']=max(1e-6,mid-half);r['ask']=mid+half;r['regime']='spread_stress'
        elif family=='chop_reversal' and i>=pivot:
            rr=(r['close']/max(r['open'],1e-12)-1)*((-1)**(i-pivot));new=max(1e-6,float(r['open'])*(1+rr*(1+sev)));r['close']=new;r['high']=max(r['open'],new)*(1+abs(rr)*0.2);r['low']=max(1e-6,min(r['open'],new)*(1-abs(rr)*0.2));mid=new;half=max(1e-8,(r['ask']-r['bid'])/2);r['bid']=mid-half;r['ask']=mid+half;r['regime']='chop_stress'
        elif family=='regime_break' and i>=pivot:r['regime']='unseen_transition_stress';r['liquidity']=clamp(float(r['liquidity'])-0.2*sev)
        elif family=='execution_degradation' and i>=pivot:
            mid=float(r['close']);half=(float(r['ask'])-float(r['bid']))*(1+2*sev)/2;r['bid']=max(1e-6,mid-half);r['ask']=mid+half;r['liquidity']=clamp(float(r['liquidity'])*(1-0.45*sev));r['regime']='execution_stress'
    seed=int(content_hash({'base':path['path_id'],'family':family,'severity':severity,'index':index})[:16],16);q['path_id']=stable_id('stress_path',{'base':path['path_id'],'family':family,'severity':severity,'index':index});q['origin']='synthetic_stress';q['generator_id']=f'stress::{family}';q['seed']=seed;q['stress_labels']=list(path.get('stress_labels',[]))+[{'family':family,'severity':sev,'pivot_index':pivot}];q['watermark']=make(q['generator_id'],seed,path['source_hash']);q['parent_path_id']=path['path_id'];return q
def compose_stress_library(base_paths,contract_mapping,ledger=None):
    c=StressProgramContract.from_mapping(contract_mapping);out=[]
    for family in c.families:
        for sev in c.severity_levels:
            for i,p in enumerate(base_paths):
                if len(out)>=c.maximum_stress_paths:break
                out.append(apply_stress(p,family,sev,i))
                if ledger:ledger.consume('stress_paths',1)
            if len(out)>=c.maximum_stress_paths:break
        if len(out)>=c.maximum_stress_paths:break
    doc={'families':list(c.families),'severity_levels':list(c.severity_levels),'path_count':len(out),'paths':out,'research_only':True,'synthetic_positive_evidence':False};doc['stress_library_hash']=content_hash(out);return doc
