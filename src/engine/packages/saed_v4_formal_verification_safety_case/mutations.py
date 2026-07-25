from __future__ import annotations
from .canonical import content_hash,stable_id
from .contracts import require_exact,require_list,require_unique
from .model import mutate_model,compile_model,explore
from .properties import check_invariants,check_temporal

MUT_KEYS=["mutation_id","description","operation","transition_id","field","value","expression","transition","expected_detectors"]

def run_mutations(base_spec:dict,mutations:list,invariants:dict,temporal:dict)->tuple[dict,dict]:
    require_list(mutations,"mutations",1); require_unique(mutations,"mutation_id","mutations")
    records=[]; counterexamples=[]
    for mutation in mutations:
        require_exact(mutation,MUT_KEYS,name="mutation")
        compiled=compile_model(mutate_model(base_spec,mutation)); graph=explore(compiled)
        inv=check_invariants(graph,invariants); temp=check_temporal(graph,temporal)
        failed={x["invariant_id"] for x in inv["results"] if not x["passed"]}|{x["property_id"] for x in temp["results"] if not x["passed"]}
        expected=set(mutation["expected_detectors"]); killed=bool(failed & expected)
        records.append({"mutation_id":mutation["mutation_id"],"killed":killed,"expected_detectors":mutation["expected_detectors"],"observed_detectors":sorted(failed),"mutant_model_hash":compiled["model_hash"]})
        for result in inv["results"]+temp["results"]:
            if not result["passed"]:
                counterexamples.append({"mutation_id":mutation["mutation_id"],"detector_id":result.get("invariant_id",result.get("property_id")),"counterexamples":result["counterexamples"],"minimal_by_breadth_first_reachability":True})
    killed=sum(x["killed"] for x in records)
    score={"phase":"SAED_V4_31","mutation_count":len(records),"killed_count":killed,"survivor_count":len(records)-killed,"score":killed/len(records),"records":records,"required_score":1.0,"passed":killed==len(records),"research_only":True}
    score["scorecard_id"]=stable_id("v431_mutation_scorecard",score); score["scorecard_hash"]=content_hash(score)
    ledger={"phase":"SAED_V4_31","entries":counterexamples,"entry_count":len(counterexamples),"all_failures_preserved":True,"counterexample_discard_allowed":False,"research_only":True}
    ledger["ledger_id"]=stable_id("v431_counterexample_ledger",ledger); ledger["ledger_hash"]=content_hash(ledger)
    return score,ledger
