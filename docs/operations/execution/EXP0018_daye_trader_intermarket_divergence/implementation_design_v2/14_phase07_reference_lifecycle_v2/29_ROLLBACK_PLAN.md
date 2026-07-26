# Rollback plan

1. stop the P07 Expert;
2. preserve audit and checkpoint evidence;
3. remove only files listed in the patch manifest;
4. restore the prior P06 `DAYE_ConfirmationEngine.mqh` if P07 is removed;
5. do not reinterpret existing accepted uses after rollback;
6. rerun P06 validation and compile gates.
