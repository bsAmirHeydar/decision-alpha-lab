from tools.repository_paths import find_repository_root
from pathlib import Path
ROOT=find_repository_root(__file__)
INC=ROOT/'mql5/Include/AlphaLab/StrategyFactory/Portfolio'
EXP=ROOT/'mql5/Experts/AlphaLab/StrategyFactory/Diagnostics'
def test_mql5_portfolio_contract_files_exist(): assert len(list(INC.glob('*.mqh')))>=13 and len(list(EXP.glob('EXP_UCE_I17_*.mq5')))>=3
def test_mql5_authority_is_denied():
 t=(INC/'PortfolioCatalog.mqh').read_text();assert '#define AL_PORTFOLIO_ORDER_AUTHORITY false' in t and '#define AL_PORTFOLIO_BROKER_AUTHORITY false' in t and '#define AL_PORTFOLIO_NETWORK_AUTHORITY false' in t
def test_mql5_gate_rejects_unreserved_risk_source(): assert 'selected_risk-reserved_risk' in (INC/'PortfolioAllocator.mqh').read_text()
