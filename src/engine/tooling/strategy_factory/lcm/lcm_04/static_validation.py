from pathlib import Path

def validate(repo_root: Path):
    root=repo_root/'src/engine/tooling/strategy_factory/lcm/lcm_04'
    forbidden=['Order'+'Send(','C'+'Trade ','Web'+'Request(','Position'+'Open(','git add'+ ' .','git add'+ ' -A']
    findings=[]
    for p in root.rglob('*.py'):
        if p.name == 'static_validation.py':
            continue
        text=p.read_text(encoding='utf-8')
        for token in forbidden:
            if token in text: findings.append({'path':p.relative_to(repo_root).as_posix(),'token':token})
    return {'passed':not findings,'finding_count':len(findings),'findings':findings}
