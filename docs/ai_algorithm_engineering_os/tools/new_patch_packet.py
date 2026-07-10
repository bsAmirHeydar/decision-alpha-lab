#!/usr/bin/env python3
"""Create a complete patch packet inside a project folder.

Usage:
    python tools/new_patch_packet.py PATCH-ID "Patch Title" [output_root]

Example:
    python tools/new_patch_packet.py DIV-EXT-001 "Consumed Extreme State" ./work
"""
from __future__ import annotations
import re
import shutil
import sys
from datetime import date
from pathlib import Path

VAULT = Path(__file__).resolve().parents[1]
TEMPLATES = VAULT / '14_TEMPLATES'
FILES = {
    '01_spec.md': '01_Algorithm_Spec_Template.md',
    '02_context_packet.md': '12_AI_Context_Packet_Template.md',
    '03_patch_manifest.md': '05_Patch_Manifest_Template.md',
    '04_test_matrix.md': '07_Test_Matrix_Template.md',
    '05_review.md': '11_Code_Review_Template.md',
    '06_release_checklist.md': '../15_CHECKLISTS/01_Master_Feature_Checklist.md',
    '07_engineering_log.md': '15_Daily_Engineering_Log_Template.md',
}

def safe_slug(value: str) -> str:
    value = re.sub(r'[^A-Za-z0-9._-]+','-',value.strip())
    return value.strip('-').lower()


def main() -> int:
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    patch_id, title = sys.argv[1], sys.argv[2]
    output_root = Path(sys.argv[3]).resolve() if len(sys.argv) > 3 else Path.cwd()
    packet = output_root / f'{safe_slug(patch_id)}-{safe_slug(title)}'
    if packet.exists():
        print(f'ERROR: target exists: {packet}')
        return 1
    packet.mkdir(parents=True)
    for out_name, source_rel in FILES.items():
        source = (TEMPLATES / source_rel).resolve()
        text = source.read_text(encoding='utf-8')
        text = text.replace('[PATCH-ID]', patch_id).replace('[Feature/Patch]', f'{patch_id} — {title}')
        text = text.replace('[Algorithm Name]', title).replace('[Task ID]', patch_id)
        text = text.replace('[YYYY-MM-DD]', date.today().isoformat())
        (packet/out_name).write_text(text, encoding='utf-8', newline='\n')
    (packet/'README.md').write_text(f'''# {patch_id} — {title}\n\n## Execution Order\n1. Complete `01_spec.md`.\n2. Prepare `02_context_packet.md`.\n3. Finalize scope in `03_patch_manifest.md`.\n4. Define evidence in `04_test_matrix.md`.\n5. Implement and record work in `07_engineering_log.md`.\n6. Conduct independent review in `05_review.md`.\n7. Pass `06_release_checklist.md`.\n\nCreated: {date.today().isoformat()}\n''', encoding='utf-8')
    print(packet)
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
