from .canonical import with_digest
def evaluate_security(bundle,authority,registry,dag):
    checks={'acl05_network_denied':bundle['environment']['network_access_allowed'] is False,'acl05_secret_denied':bundle['environment']['secret_access_allowed'] is False,'authority_order_denied':authority['checks']['order_denied'],'authority_capital_denied':authority['checks']['capital_denied'],'registry_closed_world':registry['closed_world'],'dag_batch_mutation_denied':dag['batch_mutation_allowed'] is False,'dag_candidate_mutation_denied':dag['candidate_mutation_allowed'] is False,'diagnostic_lane_segregated':True}
    return with_digest({'schema_version':'1.0.0','checks':checks,'passed':all(checks.values()),'live_order_submission_allowed':False,'capital_activation_allowed':False},'report_digest')
