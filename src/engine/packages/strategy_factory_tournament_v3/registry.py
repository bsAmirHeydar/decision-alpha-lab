from .treatments import default_treatment_universe
from .algorithms import default_algorithm_universe
CAPABILITIES={'exp0017_adapter':True,'hook_zone_adapter':True,'frozen_treatment_families':9,'algorithm_families':8,'prospective_reconciliation':True,'real_market_data_embedded':False,'broker_execution_authority':False}
def capability_manifest():return {'version':'1.0.0','capabilities':CAPABILITIES}
