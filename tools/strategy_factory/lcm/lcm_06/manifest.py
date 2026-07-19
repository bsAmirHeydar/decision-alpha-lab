from .canonical import sha256_bytes,digest_object
def build(root):
    rows=[]
    for p in sorted(root.rglob('*')):
        if p.is_file() and p.name!='output_manifest.json':rows.append({"path":p.relative_to(root).as_posix(),"size_bytes":p.stat().st_size,"sha256":sha256_bytes(p.read_bytes())})
    obj={"schema_version":"1.0.0","artifact_count":len(rows),"artifacts":rows,"output_manifest_digest":None};obj['output_manifest_digest']=digest_object(obj,'output_manifest_digest');return obj
