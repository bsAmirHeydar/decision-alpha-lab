---
type: checklist
project: EXP0017
phase: 10
hotfix: 001
---

# Phase 10 Hotfix001 Compile Checklist

- [ ] Install the patch at repository root.
- [ ] Recompile `EXP0017_CG_Model_Dataset_Anatomy.mq5`.
- [ ] Confirm no `lvalue expected` errors remain in `CGM_Types.mqh`.
- [ ] Confirm no `lvalue expected` error remains in `CGM_FeatureBuilder.mqh`.
- [ ] Confirm no implicit `unknown` to `string` warnings remain at the corrected lines.
- [ ] Verify lowercase boolean inputs still parse correctly.
- [ ] Verify direction values map as BUY=1 and SELL=-1.
- [ ] Verify side values map as LOW=1 and HIGH=-1.
- [ ] Verify availability values match `COMPLETE` case-insensitively.
