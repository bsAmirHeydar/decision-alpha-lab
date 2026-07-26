# Lifecycle algorithm

```text
for each unseen P06 result:
    remember result id
    if not immutable confirmed result: ignore
    resolve reference id
    activate if absent
    if retired: reject
    else if protected role changed: retire and reject
    else if exact opportunity already accepted: suppress duplicate
    else: accept use and keep protected-survives state

for each surviving reference:
    inspect newer matching P05 observations
    if protected did not hunt: survive
    if both hunted: retire double-hunt
    else if previous protected is now hunter: retire role-switch
    else if protected hunted: retire protected-touch
```
