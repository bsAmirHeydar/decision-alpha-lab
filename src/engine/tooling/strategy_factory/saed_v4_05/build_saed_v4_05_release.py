from tools.repository_paths import find_repository_root
from pathlib import Path
import sys
import zipfile

ROOT = find_repository_root(__file__)
output = (
    Path(sys.argv[1])
    if len(sys.argv) > 1
    else ROOT.parent / "decision-alpha-lab-saed-v4-05-semantic-temporal-hypergraph-v1.0.0.zip"
)
paths = [line.strip() for line in (ROOT / "releases/history/saed/indexes/SAED_V4_05_FILE_INDEX.txt").read_text(encoding="utf-8").splitlines() if line.strip()]
with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
    for relative in paths:
        source = ROOT / relative
        if not source.is_file():
            raise SystemExit(f"indexed file missing: {relative}")
        archive.write(source, relative)
print(output)
