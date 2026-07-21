from __future__ import annotations
from typing import Any
from .errors import ContractError
ALLOWED={"const","exists","eq","ne","gt","gte","lt","lte","in","all","any","not"}

def resolve(path:str,env:dict[str,Any])->Any:
    cur:Any=env
    for part in path.split("."):
        if not isinstance(cur,dict) or part not in cur:return None
        cur=cur[part]
    return cur

def validate_expression(expr:dict[str,Any])->None:
    if not isinstance(expr,dict) or set(expr)!={"op","args"}:raise ContractError("LCM09B_EXPRESSION_SHAPE_INVALID")
    op=expr["op"];args=expr["args"]
    if op not in ALLOWED or not isinstance(args,list):raise ContractError("LCM09B_EXPRESSION_OPERATOR_INVALID")
    if op in {"all","any"}:
        if not args:raise ContractError("LCM09B_EXPRESSION_EMPTY_GROUP")
        for x in args:validate_expression(x)
    elif op=="not":
        if len(args)!=1:raise ContractError("LCM09B_EXPRESSION_ARITY")
        validate_expression(args[0])
    elif op=="const":
        if len(args)!=1 or not isinstance(args[0],bool):raise ContractError("LCM09B_EXPRESSION_CONST_INVALID")
    elif op=="exists":
        if len(args)!=1 or not isinstance(args[0],str):raise ContractError("LCM09B_EXPRESSION_EXISTS_INVALID")
    elif len(args)!=2 or not isinstance(args[0],str):raise ContractError("LCM09B_EXPRESSION_COMPARISON_INVALID")

def evaluate_expression(expr:dict[str,Any],env:dict[str,Any])->bool:
    validate_expression(expr);op=expr["op"];args=expr["args"]
    if op=="const":return args[0]
    if op=="exists":return resolve(args[0],env) is not None
    if op=="all":return all(evaluate_expression(x,env) for x in args)
    if op=="any":return any(evaluate_expression(x,env) for x in args)
    if op=="not":return not evaluate_expression(args[0],env)
    lhs=resolve(args[0],env);rhs=args[1]
    if lhs is None:return False
    if op=="eq":return lhs==rhs
    if op=="ne":return lhs!=rhs
    if op=="gt":return lhs>rhs
    if op=="gte":return lhs>=rhs
    if op=="lt":return lhs<rhs
    if op=="lte":return lhs<=rhs
    if op=="in":return lhs in rhs
    raise ContractError("LCM09B_EXPRESSION_UNREACHABLE")
