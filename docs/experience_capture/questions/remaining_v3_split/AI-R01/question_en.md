# AI-R01 — AI Boundary and Allowed Decisions

## Purpose
چون AI نباید ontology را خراب کند یا نقش decision god بگیرد. باید دقیق مشخص شود AI چه کارهایی مجاز است انجام دهد و چه چیزهایی hard rule باقی می‌ماند.

## Required Clarifications
- AI مجاز است ontology را تغییر دهد یا فقط پیشنهاد بدهد؟
- AI فقط rank/veto/select/score می‌کند؟
- AI می‌تواند zone family جدید پیشنهاد دهد؟
- AI می‌تواند entry را replace کند؟
- AI می‌تواند risk budget پیشنهاد دهد؟
- AI می‌تواند order send کند؟ طبق معماری فعلی جواب پیش‌فرض: نه.
- چه چیزهایی hard rule هستند؟
- چه چیزهایی learnable policy هستند؟
- AI output باید explainable باشد؟
- هر تصمیم AI چطور audit می‌شود؟

## Image Requirement
خیر. پاسخ متنی کافی است.

## Expected Derived Outputs
- `ai_boundary_model_v1.csv`
- `ai_allowed_actions_v1.csv`
- `ai_veto_rank_select_policy_v1.csv`
- `ai_audit_contract_v1.csv`
