from .contracts import TreatmentAtomDescriptor,AtomCompatibility
from .enums import TreatmentKind,AtomOwner
from .parameters import ParameterSchema
def descriptor(atom_id:str,kind:TreatmentKind,family:str,schema:ParameterSchema,*,required=(),owner=AtomOwner.CORE,description='',version='1.0.0'):
    return TreatmentAtomDescriptor(atom_id,version,kind,family,owner,f'python:{atom_id}:{version}',schema,AtomCompatibility(required_context_fields=tuple(required)),description)
