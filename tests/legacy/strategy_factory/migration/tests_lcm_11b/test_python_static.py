import ast
def test_python_static(repo_root):
 root=repo_root/"src/engine/tooling/strategy_factory/lcm/lcm_11b";files=list(root.glob("*.py"));assert len(files)>=20
 for p in files:ast.parse(p.read_text(encoding="utf-8"),filename=str(p))
