from __future__ import annotations
from typing import Any
from .budget import ResearchLedger
from .canonical import content_hash, stable_id
from .contracts import SparseDictionaryContract
from .model import forward
from .numerics import mean

def run(records:list[dict[str,Any]], contract:SparseDictionaryContract, ledger:ResearchLedger)->dict[str,Any]:
    vectors=[forward(r)["layer2"] for r in records]
    dim=len(vectors[0]); variances=[]
    for j in range(dim):
        m=mean(v[j] for v in vectors); variances.append(mean((v[j]-m)**2 for v in vectors))
    order=sorted(range(dim),key=lambda j:(-variances[j],j))[:contract.dictionary_size]
    atoms=[]
    for atom_id,j in enumerate(order):
        basis=[0.0]*dim; basis[j]=1.0; atoms.append({"atom_id":f"atom_{atom_id:03d}","source_dimension":j,"basis":basis,"variance":variances[j]})
        ledger.consume("dictionary_trials",1,{"source_dimension":j})
    errors=[]; encodings=[]
    for r,v in zip(records,vectors):
        active=sorted(order,key=lambda j:(-abs(v[j]),j))[:contract.top_k]; recon=[0.0]*dim
        for j in active: recon[j]=v[j]
        err=mean((a-b)**2 for a,b in zip(v,recon)); errors.append(err)
        encodings.append({"record_id":r["record_id"],"active_atoms":[{"source_dimension":j,"coefficient":v[j]} for j in active],"reconstruction_error":err})
    random_error=mean(sum(x*x for x in v)/dim for v in vectors)
    payload={"phase":"SAED_V4_26","dictionary_size":len(atoms),"top_k":contract.top_k,"atoms":atoms,"encodings":encodings,"mean_reconstruction_error":mean(errors),"random_control_error":random_error,"reference_gate_passed":mean(errors)<=contract.maximum_reconstruction_error and mean(errors)<random_error,"claim_class":"sparse_dictionary_research_challenger"}
    payload["dictionary_report_id"]=stable_id("sparse_dictionary",payload); payload["dictionary_report_hash"]=content_hash(payload)
    return payload
