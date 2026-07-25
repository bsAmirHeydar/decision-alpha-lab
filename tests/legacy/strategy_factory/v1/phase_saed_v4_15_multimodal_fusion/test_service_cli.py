import subprocess,sys
def test_cli(root):
 r=subprocess.run([sys.executable,'-m','saed_v4_multimodal_fusion.cli'],cwd=root,env={**__import__('os').environ,'PYTHONPATH':str(root/'src/engine/packages')},capture_output=True,text=True);assert r.returncode==0 and 'SAED_V4_15' in r.stdout and 'handoff_hash' in r.stdout
