from saed_v4_self_supervised_pretraining.corpus import build_corpus_manifest,corpus_membership

def test_corpus_manifest(records,upstream):
 m=build_corpus_manifest(records,*upstream);assert m['record_count']==len(records);assert m['self_supervised_only'];assert not m['outcome_inputs_allowed']
def test_manifest_deterministic(records,upstream):assert build_corpus_manifest(records,*upstream)['manifest_hash']==build_corpus_manifest(records,*upstream)['manifest_hash']
def test_membership_complete(records):
 m=corpus_membership(records);assert m['record_count']==len(records);assert len({x['record_hash'] for x in m['entries']})==len(records)
def test_synthetic_watermark(records,upstream):assert build_corpus_manifest(records,*upstream)['synthetic_reference_only']
