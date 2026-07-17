from __future__ import annotations
from collections import deque
from copy import deepcopy
from typing import Any
from .canonical import content_hash,stable_id
from .contracts import require_exact,require_list,require_unique
from .expression import evaluate,evaluate_value,compile_expression
from .errors import ModelError

MODEL_KEYS=["phase","model_name","variables","initial_state","transitions","max_depth","research_only"]
VAR_KEYS=["name","domain","description"]
TRANSITION_KEYS=["transition_id","action","guard","effects","authority_free","description"]

def compile_model(spec:dict)->dict:
    require_exact(spec,MODEL_KEYS,name="formal_model")
    if spec["phase"]!="SAED_V4_31" or spec["research_only"] is not True: raise ModelError("phase and research_only required")
    variables=require_list(spec["variables"],"variables",1); require_unique(variables,"name","variables")
    domains={}
    for item in variables:
        require_exact(item,VAR_KEYS,name="variable")
        domain=require_list(item["domain"],f"domain:{item['name']}",2)
        if len(domain)!=len({repr(x) for x in domain}): raise ModelError("duplicate domain value")
        domains[item["name"]]=domain
    require_exact(spec["initial_state"],domains,name="initial_state")
    for name,value in spec["initial_state"].items():
        if value not in domains[name]: raise ModelError(f"initial value outside domain: {name}")
    transitions=require_list(spec["transitions"],"transitions",1); require_unique(transitions,"transition_id","transitions")
    actions=[]
    for transition in transitions:
        require_exact(transition,TRANSITION_KEYS,name="transition")
        if transition["authority_free"] is not True: raise ModelError("all transitions must be authority-free")
        if not isinstance(transition["effects"],dict) or not transition["effects"]: raise ModelError("effects required")
        unknown=set(transition["effects"])-set(domains)
        if unknown: raise ModelError(f"unknown effect variables {sorted(unknown)}")
        compile_expression(transition["guard"],set(domains))
        for name,expression in transition["effects"].items():
            value=evaluate_value(expression,spec["initial_state"])
            if value not in domains[name]: raise ModelError(f"effect outside domain: {name}")
        actions.append(transition["action"])
    if len(actions)!=len(set(actions)): raise ModelError("actions must be unique")
    if not isinstance(spec["max_depth"],int) or not (1<=spec["max_depth"]<=64): raise ModelError("invalid max_depth")
    body=deepcopy(spec); body["variable_domains"]=domains; body["model_id"]=stable_id("v431_formal_model",spec); body["model_hash"]=content_hash(spec)
    return body

def state_key(state:dict,order:list[str])->tuple:
    return tuple(state[name] for name in order)

def apply_transition(state:dict,transition:dict,domains:dict)->dict:
    if not evaluate(transition["guard"],state): raise ModelError("transition guard is false")
    post=dict(state)
    for name,expression in transition["effects"].items():
        value=evaluate_value(expression,state)
        if value not in domains[name]: raise ModelError(f"effect outside domain: {name}")
        post[name]=value
    return post

def explore(model:dict)->dict:
    order=[x["name"] for x in model["variables"]]; domains=model["variable_domains"]
    initial=dict(model["initial_state"]); initial_key=state_key(initial,order)
    queue=deque([(initial,0)]); seen={initial_key:initial}; paths={initial_key:[]}; edges=[]
    while queue:
        state,depth=queue.popleft()
        source_key=state_key(state,order)
        if depth>=model["max_depth"]: continue
        for transition in model["transitions"]:
            if evaluate(transition["guard"],state):
                post=apply_transition(state,transition,domains); target_key=state_key(post,order)
                edge={"source_key":list(source_key),"target_key":list(target_key),"transition_id":transition["transition_id"],"action":transition["action"],"authority_free":transition["authority_free"]}
                edges.append(edge)
                if target_key not in seen:
                    seen[target_key]=post; paths[target_key]=paths[source_key]+[transition["transition_id"]]; queue.append((post,depth+1))
    states=[]
    for key,state in sorted(seen.items(),key=lambda x:repr(x[0])):
        record={"state_id":stable_id("v431_state",state),"values":state,"shortest_transition_path":paths[key],"terminal":not any(evaluate(t["guard"],state) for t in model["transitions"])}
        states.append(record)
    id_by_key={tuple(x["values"][n] for n in order):x["state_id"] for x in states}
    for edge in edges:
        edge["source_state_id"]=id_by_key[tuple(edge.pop("source_key"))]; edge["target_state_id"]=id_by_key[tuple(edge.pop("target_key"))]
        edge["edge_hash"]=content_hash(edge)
    body={"phase":"SAED_V4_31","model_id":model["model_id"],"model_hash":model["model_hash"],"initial_state_id":id_by_key[initial_key],"state_count":len(states),"transition_instance_count":len(edges),"states":states,"edges":sorted(edges,key=lambda x:(x["source_state_id"],x["transition_id"],x["target_state_id"])),"bounded_depth":model["max_depth"],"complete_for_reachable_finite_state_space":True,"research_only":True}
    body["graph_id"]=stable_id("v431_reachability_graph",body); body["graph_hash"]=content_hash(body); return body

def mutate_model(model_spec:dict,mutation:dict)->dict:
    result=deepcopy(model_spec); op=mutation["operation"]
    transitions={x["transition_id"]:x for x in result["transitions"]}
    if op=="set_initial": result["initial_state"][mutation["field"]]=mutation["value"]
    elif op=="set_effect": transitions[mutation["transition_id"]]["effects"][mutation["field"]]=mutation["expression"]
    elif op=="set_guard": transitions[mutation["transition_id"]]["guard"]=mutation["expression"]
    elif op=="drop_transition": result["transitions"]=[x for x in result["transitions"] if x["transition_id"]!=mutation["transition_id"]]
    elif op=="add_transition": result["transitions"].append(deepcopy(mutation["transition"]))
    else: raise ModelError(f"unknown mutation operation {op}")
    return result
