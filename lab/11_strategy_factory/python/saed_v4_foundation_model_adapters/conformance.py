from .authority import assert_operation
from .errors import V414Error

def execute_vectors(vectors):
    rows=[]
    for v in vectors:
        passed=False;error=''
        try:
            result=assert_operation(v['operation']);passed=(result is True)==v['expect_allowed']
        except Exception as e:
            error=type(e).__name__;passed=not v['expect_allowed']
        rows.append({'vector_id':v['vector_id'],'operation':v['operation'],'expected_allowed':v['expect_allowed'],'passed':passed,'error':error})
    return {'phase':'SAED_V4_14','rows':rows,'passed':all(r['passed'] for r in rows)}
