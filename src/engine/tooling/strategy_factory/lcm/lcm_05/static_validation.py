import json
def validate(repo_root):
    policies=list((repo_root/'registry/history/lcm/lcm_05/policies').glob('*.json'));[json.loads(p.read_text(encoding='utf-8')) for p in policies];forbidden=[]
    for p in (repo_root/'src/engine/tooling/strategy_factory/lcm/lcm_05').glob('*.py'):
        if p.name=='static_validation.py':continue
        t=p.read_text(encoding='utf-8')
        for token in ['OrderSend(','CTrade','WebRequest(','subprocess.Popen(','shell=True']:
            if token in t:forbidden.append({'path':p.as_posix(),'token':token})
    return {"passed":not forbidden,"policy_count":len(policies),"forbidden_findings":forbidden}
