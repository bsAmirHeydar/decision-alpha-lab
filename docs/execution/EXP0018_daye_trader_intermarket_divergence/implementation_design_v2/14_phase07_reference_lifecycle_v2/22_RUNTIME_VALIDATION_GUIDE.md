# Runtime validation guide

1. Compile P07 with 0 errors and 0 warnings.
2. Keep P06 and P07 checkpoints enabled.
3. Confirm first one-sided close creates one accepted use and one surviving reference.
4. Confirm repeated timer callbacks do not create another use.
5. Confirm a later distinct opportunity can add a use while protected remains clean.
6. Confirm protected touch retires the reference.
7. Confirm no later confirmation reactivates or reuses the retired reference.
8. Inspect optional audit CSV and Common Files checkpoint.
