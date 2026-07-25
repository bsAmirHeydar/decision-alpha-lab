import json,pytest

def validate(v,s,path='$'):
    t=s.get('type')
    if t=='object':
        assert isinstance(v,dict),path;assert set(s.get('required',[]))<=set(v),path
        if s.get('additionalProperties') is False:assert set(v)<=set(s.get('properties',{})),path
        for k,x in v.items():validate(x,s['properties'][k],path+'.'+k)
    elif t=='array':
        assert isinstance(v,list),path
        for i,x in enumerate(v):validate(x,s.get('items',{}),f'{path}[{i}]')
    elif t=='boolean':assert isinstance(v,bool),path
    elif t=='integer':assert isinstance(v,int) and not isinstance(v,bool),path
    elif t=='number':assert isinstance(v,(int,float)) and not isinstance(v,bool),path
    elif t=='string':assert isinstance(v,str),path
    elif t=='null':assert v is None,path

def test_schema_pairs(root):
    dirs=[root/'examples/legacy/strategy_factory/saed_v4_22',root/'releases/history/strategy_factory/artifacts/saed_v4_22'];schema=root/'schemas/legacy/strategy_factory/saed_v4_22'
    for d in dirs:
        for p in d.glob('*.JSON'):
            sp=schema/(p.stem+'.SCHEMA.JSON');assert sp.exists(),p.name;validate(json.loads(p.read_text()),json.loads(sp.read_text()))
@pytest.mark.parametrize('name',['GOLDEN_GENERATIVE_STRESS_CERTIFICATE','GOLDEN_REPLAY_RECEIPT','V4_22_TO_V4_23_HANDOFF','AUTHORITY_BOUNDARY','MODEL_RISK_REVIEW','SECURITY_REVIEW'])
def test_material_artifact_exists(root,name):assert (root/f'releases/history/strategy_factory/artifacts/saed_v4_22/{name}.JSON').exists()
