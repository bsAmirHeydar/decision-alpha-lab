from pathlib import Path
import hashlib,re,sys,yaml

def scaffold(root:Path, context_id:str, version:str="1.0.0"):
 safe=re.sub(r"[^A-Za-z0-9_-]+","_",context_id).strip("_"); out=root/f"docs/history/systems/strategy_factory_context_cells_v4/{safe}/{version}"; out.mkdir(parents=True,exist_ok=True)
 spec={"schema_version":"4.0.0","context_id":context_id,"context_version":version,"digital_twin_state":"proposed","authority":{"order":False,"risk":False,"promotion":False,"runtime_activation":False}}
 raw=yaml.safe_dump(spec,sort_keys=True); (out/"context_cell_v4.yaml").write_text(raw,encoding="utf-8"); (out/"CELL_HASH.txt").write_text(hashlib.sha256(raw.encode()).hexdigest()+"\n")
 return out
if __name__=="__main__": print(scaffold(Path(sys.argv[1]),sys.argv[2],sys.argv[3] if len(sys.argv)>3 else "1.0.0"))
