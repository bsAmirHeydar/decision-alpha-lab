---
id: EXP0018-P02-PARTIAL-DATA
title: "P02 Partial Data and Fail-Closed Semantics"
type: contract
status: active
project: EXP0018
---
# داده ناقص و fail-closed

سه حالت مستقل وجود دارد:

1. aligned and complete
2. aligned but partial
3. unavailable

`PARTIAL_ALIGNMENT` می‌تواند با `require_complete_alignment=false` برای پژوهش publish شود، اما unmatched counts باید حفظ شوند. Downstream P05 حق ندارد timestamp بدون pair را «طرف دوم هانت نکرد» تفسیر کند.

قاعده: **No Data is a third state, not False.**
