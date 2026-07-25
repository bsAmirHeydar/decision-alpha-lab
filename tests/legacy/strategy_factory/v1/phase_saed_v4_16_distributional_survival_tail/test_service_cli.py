import subprocess,sys,os
def test_cli(root):
 r=subprocess.run([sys.executable,'-m','saed_v4_distributional_survival_tail.cli'],cwd=root,env={**os.environ,'PYTHONPATH':str(root/'src/engine/packages')},capture_output=True,text=True);assert r.returncode==0 and 'SAED_V4_16' in r.stdout and 'handoff_hash' in r.stdout and 'production_authority' in r.stdout
