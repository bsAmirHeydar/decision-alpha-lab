from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from .wire import *
from .hashing import sha256_bytes, fnv1a64, stable_id

@dataclass(frozen=True, slots=True)
class LinearScalarParameters:
    weights: tuple[float, ...]
    bias: float
    def validate(self) -> None:
        if not self.weights or len(self.weights)>4096: raise ValueError("invalid linear width")
        import math
        if any(not math.isfinite(x) for x in (*self.weights,self.bias)): raise ValueError("non-finite parameter")

def export_linear_scalar_onnx(parameters: LinearScalarParameters, *, producer_version: str="0.15.0") -> bytes:
    parameters.validate(); n=len(parameters.weights)
    nodes=[node("MatMul",["features","weights"],["linear_mm"],"LinearMatMul"),
           node("Add",["linear_mm","bias"],["score"],"LinearBias")]
    graph=b"".join(bfield(1,x) for x in nodes)+sfield(2,"AlphaLabLinearScalarV1")
    graph+=bfield(5,tensor("weights",[n,1],parameters.weights))
    graph+=bfield(5,tensor("bias",[1],[parameters.bias]))
    graph+=bfield(11,value_info("features",[1,n]))+bfield(12,value_info("score",[1,1]))
    opset=sfield(1,"")+vfield(2,13)
    return (vfield(1,8)+sfield(2,"decision-alpha-lab")+sfield(3,producer_version)+vfield(5,1)+
            bfield(7,graph)+bfield(8,opset))

def export_to_file(parameters: LinearScalarParameters, path: str|Path) -> dict:
    data=export_linear_scalar_onnx(parameters); p=Path(path); p.parent.mkdir(parents=True,exist_ok=True); p.write_bytes(data)
    return {"path":str(p),"size_bytes":len(data),"sha256":sha256_bytes(data),"fnv1a64":fnv1a64(data),
            "export_id":stable_id("oxpt",sha256_bytes(data),len(parameters.weights))}

def inspect_linear_scalar_onnx(data: bytes) -> dict:
    graph=None; ir=None; opset=None
    for field,wire,value in iter_fields(data):
        if field==1 and wire==0: ir=value
        elif field==7 and wire==2: graph=value
        elif field==8 and wire==2:
            for sf,sw,sv in iter_fields(value):
                if sf==2 and sw==0: opset=sv
    if graph is None: raise ValueError("missing graph")
    operators=[]; inputs=[]; outputs=[]; initializers=[]; graph_name=""
    for field,wire,value in iter_fields(graph):
        if field==1 and wire==2:
            op=""; name=""
            for nf,nw,nv in iter_fields(value):
                if nf==4 and nw==2: op=nv.decode()
                elif nf==3 and nw==2: name=nv.decode()
            operators.append((name,op))
        elif field==2 and wire==2: graph_name=value.decode()
        elif field==5 and wire==2:
            name=""; dims=[]; dtype=None
            for tf,tw,tv in iter_fields(value):
                if tf==1 and tw==2:
                    off=0
                    while off<len(tv): v,off=decode_varint(tv,off); dims.append(v)
                elif tf==2 and tw==0: dtype=tv
                elif tf==8 and tw==2: name=tv.decode()
            initializers.append((name,tuple(dims),dtype))
        elif field==11 and wire==2:
            for vf,vw,vv in iter_fields(value):
                if vf==1 and vw==2: inputs.append(vv.decode())
        elif field==12 and wire==2:
            for vf,vw,vv in iter_fields(value):
                if vf==1 and vw==2: outputs.append(vv.decode())
    return {"ir_version":ir,"opset":opset,"graph_name":graph_name,"operators":operators,
            "inputs":inputs,"outputs":outputs,"initializers":initializers}
