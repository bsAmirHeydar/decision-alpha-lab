from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[3];index=ROOT/'SAED_V4_10_FILE_INDEX.txt';assert index.exists();paths=[x.strip() for x in index.read_text().splitlines() if x.strip()]
missing=[x for x in paths if not (ROOT/x).is_file()];assert not missing,missing
manifest=json.loads((ROOT/'SAED_V4_10_PATCH_MANIFEST.json').read_text());assert manifest['phase']=='SAED_V4_10';assert manifest['file_count']==len(paths);assert (ROOT/'lab/11_strategy_factory/phase_status/SAED_V4_10.json').exists();print(f'V4-10 delivery validated: {len(paths)} files')
