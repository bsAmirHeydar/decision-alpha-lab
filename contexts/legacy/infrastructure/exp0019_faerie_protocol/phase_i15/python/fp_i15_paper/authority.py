from pathlib import Path
from .constants import FORBIDDEN_LIVE_TOKENS
def scan_mql5_authority(paths):
    violations=[]
    for path in paths:
        text=Path(path).read_text(encoding='utf-8',errors='ignore')
        if Path(path).name.startswith('FP_I15_') or 'FaerieProtocol_Paper' in Path(path).name:
            for token in FORBIDDEN_LIVE_TOKENS:
                if token in text: violations.append((str(path),token))
    return tuple(violations)
