from .canonical import content_hash

def boundary():
    output = {
        'phase': 'SAED_V4_24',
        'authority': {
            'decision': False,
            'promotion': False,
            'runtime': False,
            'risk_allocation': False,
            'execution': False,
            'production': False,
            'online_learning': False,
        },
        'research_only': True,
        'safe_action': 'skip',
        'ucee_authority_preserved': True,
    }
    output['boundary_hash'] = content_hash(output)
    return output
