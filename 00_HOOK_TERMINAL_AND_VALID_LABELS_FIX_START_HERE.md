# Hook Terminal and Valid Labels Fix

This patch corrects two production-view doctrines:

1. Positive Hook terminal is the lowest same-side valley reached by that Hook origin group.
2. In valid-only mode, only labels belonging to visible valid Hook groups are drawn.

Valid Hook groups are:

- immediate Hook after an opposing F3
- Hook-2 after Hook-1 when Hook-2 origin equals Hook-1 terminal
- Hook-1 only as the parent companion of a visible Hook-2
