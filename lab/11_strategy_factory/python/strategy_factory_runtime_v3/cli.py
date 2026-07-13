from __future__ import annotations
import argparse,json
from .golden import golden_bundle,golden_vectors
from .parity import certify_parity
def main(argv=None):
    p=argparse.ArgumentParser(prog='strategy-factory-runtime-v3');p.add_argument('command',choices=['golden-parity','probe-onnx']);a=p.parse_args(argv)
    if a.command=='probe-onnx':
        from .export import onnx_availability;print(json.dumps(onnx_availability(),sort_keys=True));return 0
    m,pre,model,export,data=golden_bundle();cert=certify_parity(m,pre,model,data,golden_vectors(),created_at_ms=0);print(json.dumps({'status':cert.status.value,'certificate_hash':cert.certificate_hash},sort_keys=True));return 0 if cert.status.value=='pass' else 1
if __name__=='__main__':raise SystemExit(main())
