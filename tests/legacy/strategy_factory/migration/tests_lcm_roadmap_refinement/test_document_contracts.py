import json

def test_subphase_documents_have_required_sections(repo_root):
    d=json.loads((repo_root/'registry/history/lcm/roadmaps/LCM_ROADMAP_R1_BALANCED_PARTITION/roadmap_registry.json').read_text(encoding='utf-8'))
    required=['## Purpose','## Explicit non-goals','## Entry contract','## Engineering workstreams','## Mandatory verification','## Hostile review','## Failure semantics','## Rollback requirements','## Acceptance gate','## Handoff contract']
    for r in d['records']:
        text=(repo_root/r['document_path']).read_text(encoding='utf-8')
        for section in required:
            assert section in text, (r['subphase_id'],section)
