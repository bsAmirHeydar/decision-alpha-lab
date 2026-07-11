from __future__ import annotations
import struct

def varint(value: int) -> bytes:
    if value < 0: value &= (1<<64)-1
    out=bytearray()
    while True:
        b=value & 0x7f; value >>= 7
        if value: out.append(b|0x80)
        else: out.append(b); return bytes(out)
def key(field: int, wire: int) -> bytes: return varint((field<<3)|wire)
def vfield(field: int, value: int) -> bytes: return key(field,0)+varint(value)
def bfield(field: int, data: bytes) -> bytes: return key(field,2)+varint(len(data))+data
def sfield(field: int, value: str) -> bytes: return bfield(field,value.encode())
def packed_varints(field: int, values) -> bytes: return bfield(field,b"".join(varint(v) for v in values))
def dimension(value: int) -> bytes: return vfield(1,value)
def shape(values) -> bytes: return b"".join(bfield(1,dimension(v)) for v in values)
def tensor_type(element_type: int, dims) -> bytes: return vfield(1,element_type)+bfield(2,shape(dims))
def type_proto(element_type: int, dims) -> bytes: return bfield(1,tensor_type(element_type,dims))
def value_info(name: str, dims) -> bytes: return sfield(1,name)+bfield(2,type_proto(1,dims))
def tensor(name: str, dims, values) -> bytes:
    raw=b"".join(struct.pack("<f",float(v)) for v in values)
    return packed_varints(1,dims)+vfield(2,1)+sfield(8,name)+bfield(9,raw)
def node(op_type: str, inputs, outputs, name: str) -> bytes:
    return (b"".join(sfield(1,x) for x in inputs)+b"".join(sfield(2,x) for x in outputs)+
            sfield(3,name)+sfield(4,op_type))

def decode_varint(data: bytes, offset: int):
    value=0; shift=0
    while True:
        if offset>=len(data): raise ValueError("truncated varint")
        b=data[offset]; offset+=1; value |= (b&0x7f)<<shift
        if not b&0x80: return value,offset
        shift+=7
        if shift>70: raise ValueError("oversized varint")
def iter_fields(data: bytes):
    offset=0
    while offset<len(data):
        tag,offset=decode_varint(data,offset); field=tag>>3; wire=tag&7
        if wire==0: value,offset=decode_varint(data,offset); yield field,wire,value
        elif wire==2:
            size,offset=decode_varint(data,offset); end=offset+size
            if end>len(data): raise ValueError("truncated field")
            yield field,wire,data[offset:end]; offset=end
        elif wire==5: yield field,wire,data[offset:offset+4]; offset+=4
        elif wire==1: yield field,wire,data[offset:offset+8]; offset+=8
        else: raise ValueError(f"unsupported wire type {wire}")
