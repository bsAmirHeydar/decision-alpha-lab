def test_obsidian_delivery_is_detailed(root):
 d=root/'docs/history/systems/saed_v4/62_PHASE_DELIVERIES_V4/V4_10';files=list(d.glob('*.md'));assert len(files)>=45;assert all(len(p.read_text(encoding='utf-8'))>500 for p in files)
def test_atomic_concepts_exist(root):
 d=root/'docs/history/systems/saed_v4/63_ATOMIC_CONCEPTS_V4/V4_10';assert len(list(d.glob('*.md')))>=18
