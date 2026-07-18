from __future__ import annotations
import re

def classify(name: str) -> tuple[str,str]:
    low=name.lower()
    canonical={'.editorconfig','.gitattributes','.gitignore','agents.md','contributing.md','code_of_conduct.md','license','license.md','pyproject.toml'}
    if low in canonical: return 'ROOT_CANONICAL','KNOWN_ROOT_CONTRACT'
    if low.endswith('.zip'): return 'BINARY_PATCH_OR_ARCHIVE','ZIP_EXTENSION'
    if low.startswith('commit_message'): return 'COMMIT_RECORD','NAME_PREFIX'
    if low.endswith('.ps1') or low.startswith(('install_','verify_','expand_remove')): return 'INSTALL_OR_VERIFY_SCRIPT','SCRIPT_PATTERN'
    if any(x in low for x in ('artifact_inventory','file_hashes','file_index','patch_manifest','qa_report')): return 'RELEASE_METADATA','RELEASE_SUFFIX'
    if 'manifest' in low: return 'PROGRAM_OR_RELEASE_MANIFEST','MANIFEST_NAME'
    if low.startswith('readme'): return 'ROOT_README','README_NAME'
    return 'ROOT_REVIEW_REQUIRED','NO_CLOSED_CLASS_MATCH'

def scan(records: tuple[dict,...]) -> list[dict]:
    out=[]
    for r in records:
        if '/' in r['path']: continue
        cls,reason=classify(r['path'])
        out.append({'path':r['path'],'classification':cls,'classification_reason':reason,'size_bytes':r['size_bytes'],'sha256':r['sha256'],'move_performed':False,'delete_performed':False,'review_required':cls=='ROOT_REVIEW_REQUIRED'})
    return out
