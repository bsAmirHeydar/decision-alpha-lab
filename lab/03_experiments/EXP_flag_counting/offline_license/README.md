# Offline License Lab

Use this folder to store private issuer notes and generated test bundles. Do not commit real customer tokens, passwords, account numbers, or gate values.

Recommended test cases:

1. valid account + valid server + future expiry => active
2. valid bundle + wrong password => blocked
3. valid bundle + one wrong numeric gate => blocked
4. valid bundle + wrong account => blocked
5. valid bundle + expired date => blocked
6. server-bound bundle on wrong server => blocked
7. server-any bundle on same account different server => active

Generator:

```powershell
python tools/flag_counting/offline_license_keygen.py --account 12345678 --server "Broker-Demo" --expires 20260901
```
