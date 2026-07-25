# Pilot Rollback

This patch does not switch consumers and does not move or delete `lab/03_experiments/EXP0015_intermarket_time_divergence/experiment.py`. Rollback removes only paths listed in `releases/history/lcm/indexes/LCM_08B_FILE_INDEX.txt` and restores modified roadmap documents from the predecessor commit. After rollback, verify the source SHA-256 remains `sha256:99e5e03a4bf30a2ab94949e2ddc6cdc1d067f0441d25dbe0dc8a138026a9bd2f` and run LCM-08A verification.
