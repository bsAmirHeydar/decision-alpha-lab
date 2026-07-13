from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
PHASE = ROOT / "lab/10_infrastructure/EXP0019_faerie_protocol/phase_i02"


def test_phase_does_not_modify_previous_context_or_shared_core_paths():
    index = ROOT / "EXP0019_FP_I02_FILE_INDEX.txt"
    if not index.exists():
        return
    forbidden = (
        "lab/10_infrastructure/EXP0017_",
        "lab/10_infrastructure/EXP0018_",
        "mql5/Include/AlphaLab/",
        "mql5/Experts/EXP0017",
        "mql5/Experts/EXP0018",
    )
    for line in index.read_text().splitlines():
        assert not line.startswith(forbidden), line


def test_phase_python_has_no_broker_network_or_chart_authority():
    forbidden = ("OrderSend", "CTrade", "requests.", "urllib", "socket.", "ObjectCreate", "PositionOpen")
    for path in (PHASE / "python/fp_i02_kernel").glob("*.py"):
        text = path.read_text()
        for token in forbidden:
            assert token not in text, (path, token)
