# Install SAED V4-08

1. Expand the patch into the repository root.
2. Run `python tools/strategy_factory/saed_v4_08/run_saed_v4_08_full_qa.py`.
3. Run `python tools/strategy_factory/saed_v4_08/validate_saed_v4_08_delivery.py`.
4. Compile the three diagnostic experts in a real Windows MetaEditor environment and retain the logs as external evidence.
5. Review the evidence boundary before any downstream V4-09 work.

The patch is additive and assumes SAED V4-07 is already installed. It never grants production authority.
