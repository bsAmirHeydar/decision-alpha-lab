$ErrorActionPreference = "Stop"
python tools/engineering/validate_alpha_lab_policy.py .
python docs/history/aieos_legacy/tools/validate_vault.py docs/history/aieos_legacy
python tools/engineering/check_mql5_compatibility.py .
python tools/engineering/audit_repository_layout.py .
