from pathlib import Path
import hashlib,json,re,sys,yaml

def scaffold(root: Path, context_id: str, version: str="1.0.0"):
    safe=re.sub(r"[^A-Za-z0-9_-]+","_",context_id).strip("_")
    out=root/f"docs/strategy_factory_context_cells/{safe}/{version}"; out.mkdir(parents=True,exist_ok=True)
    spec={"schema_version":"3.0.0","context_id":context_id,"context_version":version,"cell_state":"proposed","authority":{"order":False,"risk":False,"promotion":False}}
    raw=yaml.safe_dump(spec,sort_keys=True); (out/"cell.yaml").write_text(raw,encoding="utf-8")
    ident=hashlib.sha256(raw.encode()).hexdigest(); (out/"CELL_ID.txt").write_text(ident+"\n",encoding="utf-8")
    return out
if __name__=="__main__": print(scaffold(Path(sys.argv[1]),sys.argv[2],sys.argv[3] if len(sys.argv)>3 else "1.0.0"))
