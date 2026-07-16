from .canonical import content_hash

def receipt(config_hash, input_hashes, output_hashes):
    output = {
        'phase': 'SAED_V4_24',
        'config_hash': config_hash,
        'input_hashes': input_hashes,
        'output_hashes': output_hashes,
        'deterministic': True,
        'network_access': False,
        'random_seed': 424,
        'future_suffix_queries': 0,
        'protected_evidence_queries': 0,
        'runtime_compilations': 0,
        'order_submissions': 0,
    }
    output['replay_hash'] = content_hash(output)
    return output
