from saed_v4_self_supervised_pretraining.encoder import encoder_from_checkpoint
from saed_v4_self_supervised_pretraining.models import TokenStream
from saed_v4_self_supervised_pretraining.evaluation import collapse_metrics,temporal_retrieval,leakage_probe

def streams(load):
 return [TokenStream(x['record_id'],x['context_id'],x['root_context_id'],x['domain_id'],x['event_time'],x['known_time'],x['split'],tuple(x['tokens']),x['view_masks'],x['token_hash']) for x in load('releases/history/strategy_factory/artifacts/saed_v4_11/GOLDEN_TOKEN_STREAMS.JSON')['streams']]
def test_not_collapsed(load):
 e=encoder_from_checkpoint(load('releases/history/strategy_factory/artifacts/saed_v4_11/GOLDEN_ENCODER_CHECKPOINT.JSON'));assert not collapse_metrics(e,streams(load))['collapsed']
def test_unique_embeddings(load):
 e=encoder_from_checkpoint(load('releases/history/strategy_factory/artifacts/saed_v4_11/GOLDEN_ENCODER_CHECKPOINT.JSON'));assert collapse_metrics(e,streams(load))['unique_embedding_fraction']>=.5
def test_retrieval_is_bounded(load):
 e=encoder_from_checkpoint(load('releases/history/strategy_factory/artifacts/saed_v4_11/GOLDEN_ENCODER_CHECKPOINT.JSON'));r=temporal_retrieval(e,streams(load));assert 0<=r['recall_at_k']<=1
def test_leakage_probe_passes(load):assert load('releases/history/strategy_factory/artifacts/saed_v4_11/GOLDEN_REPRESENTATION_DOSSIER.JSON')['leakage_probe']['passed']
def test_dossier_no_alpha_claim(load):assert not load('releases/history/strategy_factory/artifacts/saed_v4_11/GOLDEN_REPRESENTATION_DOSSIER.JSON')['claims']['real_alpha']
