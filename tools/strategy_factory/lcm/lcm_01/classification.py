from __future__ import annotations
from pathlib import PurePosixPath
import re

TEXT_EXT={'.md','.py','.mq5','.mqh','.json','.jsonl','.yaml','.yml','.toml','.ini','.txt','.csv','.ps1','.xml','.html','.css','.js','.canvas','.set','.sha256','.diff','.webmanifest'}
LANGUAGE_BY_EXT={'.py':'PYTHON','.mq5':'MQL5_COMPILE_UNIT','.mqh':'MQL5_HEADER','.md':'MARKDOWN','.json':'JSON','.jsonl':'JSONL','.yaml':'YAML','.yml':'YAML','.toml':'TOML','.ps1':'POWERSHELL','.csv':'CSV','.xml':'XML','.html':'HTML','.js':'JAVASCRIPT','.css':'CSS','.canvas':'OBSIDIAN_CANVAS','.ini':'INI','.set':'MQL5_SET','.sha256':'HASH_LEDGER','.txt':'TEXT'}

def family_candidate(path: str) -> tuple[str,int]:
    p=path.replace('\\','/')
    low=p.lower()
    if '/' not in p:
        root_canonical={'.editorconfig','.gitattributes','.gitignore','agents.md','contributing.md','code_of_conduct.md','license','license.md','pyproject.toml'}
        if low in root_canonical:
            return ('REPOSITORY_ROOT_CONTROL',9500)
        if (low.endswith(('.zip','.sha256','.ps1')) or low.startswith(('commit_message','install_','verify_','readme_')) or any(token in low for token in ('artifact_inventory','file_hashes','file_index','patch_manifest','qa_report','manifest'))):
            return ('ROOT_RELEASE_AND_INSTALLATION_HISTORY',8500)
        return ('ROOT_REVIEW_REQUIRED',4000)
    if p.startswith('.github/'):
        return ('REPOSITORY_GOVERNANCE',8500)
    if p.startswith('.obsidian/'):
        return ('OBSIDIAN_VAULT_CONFIGURATION',8500)
    checks=[
      ('ACL_OS_PLATFORM',('lab/11_strategy_factory/acl_os/','tools/strategy_factory/acl_os/','docs/alpha_lab_master_architecture/context_lifecycle_os/')),
      ('LCM_CONTROL_PLANE',('legacy_context_migration','tools/strategy_factory/lcm/','lab/11_strategy_factory/migration/')),
      ('STRATEGY_FACTORY_PLATFORM',('mql5/Experts/StrategyFactory/','mql5/Experts/StrategyFactoryTests/','mql5/Include/StrategyFactory/','mql5/Include/AlphaLab/StrategyFactory/','mql5/Include/DecisionAlphaLab/StrategyFactory/')),
      ('EXP0019_FAERIE_PROTOCOL',('EXP0019','FaerieProtocol','faerie_protocol')),
      ('EXP0018_DAYE_TRADER',('EXP0018','DayeTrader','daye_trader')),
      ('EXP0017_CYCLE_GROUP',('EXP0017','IntermarketDivergenceExecution/CG','cycle_group')),
      ('EXP0016_INTERMARKET_EXECUTION',('EXP0016','IntermarketDivergenceExecution/STC','IntermarketDivergenceExecution/IMD','intermarket_divergence_execution')),
      ('EXP0015_INTERMARKET_TIME',('EXP0015','IntermarketDivergence/','intermarket_time_divergence')),
      ('FLAG_COUNTING_NDS_HOOK_ZONE',('FlagCounting','flag_counting','NDS','nds_','HOOK','Hook','hook_','obsidian_hook','obsidian_zone','hook_validity')),
      ('M_SERIES_CONTEXTS',('/M0001','/M0002','/M0003','/M0004','/M0005','/M0006','/M0007','M0001_','M0002_','M0003_','M0004_','M0005_','M0006_','M0007_')),
      ('EXECUTION_E_SERIES',('mql5/Experts/Execution/','mql5/Include/Execution/','docs/execution/E')),
      ('ASTRO_RESEARCH_EXECUTION',('Astro','astro')),
      ('ICT_STRUCTURAL_NODES',('/ICT/','StructuralNodes','structural_nodes')),
      ('RESEARCH_EXPERIMENTS',('mql5/Experts/Research/','mql5/Indicators/Research/','docs/research/','research/')),
      ('PRODUCT_LAB',('product_lab/','gartal_terminal')),
      ('PATCH_AND_RELEASE_ARCHIVE',('docs/patches/','docs/root_archive/','_patch','PATCH_MANIFEST')),
    ]
    for fam,needles in checks:
        if any(n in p for n in needles): return fam,9000
    top=p.split('/',1)[0]
    fallback={
      'docs':'DOCUMENTATION_OTHER',
      'mql5':'MQL5_OTHER',
      'tools':'TOOLING_OTHER',
      'lab':'LAB_OTHER',
      'registry':'REGISTRY_AND_MACHINE_CONTRACTS',
      'product_lab':'PRODUCT_LAB',
    }
    return (fallback.get(top,'OTHER_'+re.sub(r'[^A-Za-z0-9]+','_',top).upper()),3500)

def semantic_role(path: str, ext: str) -> tuple[str,int]:
    low=path.lower()
    if ext=='.mq5': return ('MQL5_COMPILE_ENTRY',8500)
    if ext=='.mqh': return ('MQL5_INCLUDE_MODULE',8000)
    if ext=='.py' and ('test_' in PurePosixPath(path).name.lower() or '/tests' in low): return ('TEST_SOURCE',8500)
    if ext=='.py': return ('PYTHON_SOURCE',7500)
    if low.startswith('docs/') and ext in {'.md','.canvas'}: return ('DOCUMENTATION',8000)
    if path.count('/')==0 and ('manifest' in low or 'inventory' in low or 'file_index' in low or 'qa_report' in low): return ('ROOT_RELEASE_METADATA',8500)
    if ext in {'.json','.yaml','.yml','.toml','.ini','.set'}: return ('CONFIGURATION_OR_DATA_CONTRACT',6000)
    if ext in {'.zip','.pdf','.png','.onnx','.blob'}: return ('BINARY_OR_PACKAGED_ARTIFACT',7000)
    return ('UNKNOWN_ROLE',0)

def generated_likelihood(path: str, ext: str) -> tuple[str,str]:
    low=path.lower(); name=PurePosixPath(path).name.lower()
    markers=('artifact_inventory','file_hashes','file_index','patch_manifest','qa_report','output_manifest','generated','projection','atomic_concepts','phase_deliveries','source_cards')
    if any(m in low for m in markers): return ('GENERATED_LIKELY','PATH_MARKER')
    if ext in {'.sha256'}: return ('GENERATED_LIKELY','HASH_LEDGER_EXTENSION')
    if name.startswith('commit_message') or name.startswith('install_') or name.startswith('verify_'): return ('RELEASE_PROCESS_LIKELY','ROOT_RELEASE_NAME')
    if ext in {'.mq5','.mqh','.py'}: return ('AUTHORED_LIKELY','SOURCE_EXTENSION')
    return ('MIXED_OR_UNKNOWN','INSUFFICIENT_STATIC_EVIDENCE')

def media_family(ext: str, binary: bool) -> str:
    if binary: return 'BINARY'
    if ext in {'.mq5','.mqh','.py','.js','.ps1','.css'}: return 'SOURCE_TEXT'
    if ext in {'.md','.txt','.html','.xml'}: return 'DOCUMENT_TEXT'
    if ext in {'.json','.jsonl','.yaml','.yml','.toml','.ini','.csv','.canvas','.set'}: return 'STRUCTURED_TEXT'
    return 'TEXT_OR_UNKNOWN'
