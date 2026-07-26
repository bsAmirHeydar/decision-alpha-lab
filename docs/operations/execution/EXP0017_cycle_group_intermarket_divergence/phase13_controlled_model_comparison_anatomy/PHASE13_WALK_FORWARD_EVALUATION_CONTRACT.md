# Phase 13 Walk-Forward Evaluation Contract

Phase 13 does not invent new fold boundaries. It reuses the Phase 11 fold plan.

For every usable fold:

1. select train rows by the declared train interval;
2. exclude embargo rows;
3. select test rows by the declared test interval;
4. fit encoders and models on train only;
5. predict each test row;
6. write fold-level metrics and sample-level predictions;
7. retain the fold identity in every output.

A model comparison without fixed, non-overlapping temporal folds is invalid under this contract.
