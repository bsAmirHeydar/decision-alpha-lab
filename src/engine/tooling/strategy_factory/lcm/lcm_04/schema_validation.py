from pathlib import Path
import json

def validate(repo_root: Path):
    root=repo_root/'registry/history/lcm/lcm_04/schemas/v1';bad=[];count=0
    try:
        import jsonschema
    except ImportError:
        jsonschema=None
    for p in sorted(root.glob('*.json')):
        count+=1
        try:
            obj=json.loads(p.read_text(encoding='utf-8'))
            if jsonschema: jsonschema.Draft202012Validator.check_schema(obj)
        except Exception as exc: bad.append({'path':p.as_posix(),'error':str(exc)})
    return {'passed':not bad,'schema_count':count,'failures':bad}
