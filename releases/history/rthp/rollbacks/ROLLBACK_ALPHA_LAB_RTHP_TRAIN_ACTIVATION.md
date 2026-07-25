# Rollback — RTHP Real Train Activation v1

This patch is additive. Rollback removes only the exact paths listed in `RTHP_TRAIN_ACTIVATION_FILE_INDEX.txt` and reverts the installation commit. It must not remove or alter canonical RTHP Context files, ACL-03 outputs, AI-input bindings, or shared Engine code.

Generated research-run directories under `lab/11_strategy_factory/runs/rthp/` are immutable run evidence and are not part of this patch. Preserve or archive them according to research-retention policy before any manual cleanup.
