from __future__ import annotations
import ast
from typing import Any
from .errors import VerificationError
_ALLOWED=(ast.Expression,ast.BoolOp,ast.UnaryOp,ast.Compare,ast.Name,ast.Load,ast.Constant,ast.And,ast.Or,ast.Not,ast.Eq,ast.NotEq,ast.In,ast.NotIn,ast.Lt,ast.LtE,ast.Gt,ast.GtE,ast.Tuple,ast.List)

def compile_expression(expression:str,allowed_names:set[str]):
    if not isinstance(expression,str) or not expression.strip(): raise VerificationError("expression must be non-empty string")
    try: tree=ast.parse(expression,mode="eval")
    except SyntaxError as exc: raise VerificationError(f"invalid expression: {expression}") from exc
    for node in ast.walk(tree):
        if not isinstance(node,_ALLOWED): raise VerificationError(f"forbidden expression node {type(node).__name__}")
        if isinstance(node,ast.Name) and node.id not in allowed_names: raise VerificationError(f"unknown expression name {node.id}")
    return compile(tree,"<saed-v4-31-expression>","eval")

def evaluate(expression:str,environment:dict[str,Any])->bool:
    code=compile_expression(expression,set(environment))
    result=eval(code,{"__builtins__":{}},environment)
    if not isinstance(result,bool): raise VerificationError("property expression must evaluate to bool")
    return result

def evaluate_value(expression:str,environment:dict[str,Any])->Any:
    code=compile_expression(expression,set(environment))
    return eval(code,{"__builtins__":{}},environment)
