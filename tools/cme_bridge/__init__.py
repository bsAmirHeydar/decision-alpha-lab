"""Temporary UC-03 compatibility namespace; remove after consumer cutover."""
from tools.repository_paths import find_repository_root
__path__ = [str(find_repository_root(__file__) / 'adapters/legacy/market_data/cme_bridge')]
