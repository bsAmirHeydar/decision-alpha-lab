from tools.repository_paths import find_repository_root
from pathlib import Path
ROOT=find_repository_root(__file__)
PKG=ROOT/"src/engine/packages/strategy_factory_policy_v3"
FORBIDDEN=("OrderSend(", "CTrade", "WebRequest(", "requests.get(", "requests.post(", "socket.socket", "subprocess.Popen", "os.system(", "eval(", "exec(")
def test_no_runtime_authority_tokens():
    text="\n".join(p.read_text() for p in PKG.glob("*.py"))
    assert all(t not in text for t in FORBIDDEN)
def test_ai_cannot_create_occurrence():
    text=(PKG/"engine.py").read_text(); assert "ContextOccurrence(" not in text
def test_non_ambiguous_hard_authority():
    text=(PKG/"authority.py").read_text(); assert text.index("if kill_switch")<text.index("if risk_rejected")<text.index("if manual_veto")
def test_manual_fallback_explicit(): assert "FallbackAction.MANUAL_ONLY" in (PKG/"fallback.py").read_text()
