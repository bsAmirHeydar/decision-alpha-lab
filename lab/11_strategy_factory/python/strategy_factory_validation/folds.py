from __future__ import annotations
from .enums import SplitMethod
from .models import ValidationPlan, ValidationFold, TimeRange
from .hashing import stable_id

def compile_walk_forward(plan: ValidationPlan) -> tuple[ValidationFold, ...]:
    plan.validate()
    if plan.method not in (SplitMethod.ANCHORED_WALK_FORWARD,
                            SplitMethod.ROLLING_WALK_FORWARD):
        raise ValueError("walk-forward compiler requires anchored or rolling method")
    folds: list[ValidationFold] = []
    anchor = plan.start_utc_msc + plan.train_span_msc
    ordinal = 0
    while ordinal < plan.maximum_folds:
        train_start = (plan.start_utc_msc if plan.method == SplitMethod.ANCHORED_WALK_FORWARD
                       else anchor - plan.train_span_msc)
        train_end = anchor
        purge_start = train_end
        purge_end = purge_start + plan.purge_span_msc
        validation_start = purge_end
        validation_end = validation_start + plan.validation_span_msc
        embargo_start = validation_end
        embargo_end = embargo_start + plan.embargo_span_msc
        test_start = embargo_end
        test_end = test_start + plan.test_span_msc
        if test_end > plan.end_utc_msc:
            break
        fold_id = stable_id("fold", f"{plan.plan_hash}|{ordinal}|{train_start}|{test_end}")
        fold = ValidationFold(
            fold_id=fold_id,
            ordinal=ordinal,
            train=TimeRange(train_start, train_end),
            validation=TimeRange(validation_start, validation_end),
            test=TimeRange(test_start, test_end),
            purge_before_validation=(TimeRange(purge_start, purge_end)
                                     if purge_end > purge_start else None),
            embargo_before_test=(TimeRange(embargo_start, embargo_end)
                                 if embargo_end > embargo_start else None),
            plan_hash=plan.plan_hash,
        ).with_hash()
        fold.validate()
        folds.append(fold)
        ordinal += 1
        anchor += plan.step_span_msc
    if not folds:
        raise ValueError("validation horizon cannot produce a complete fold")
    return tuple(folds)

def role_for_timestamp(fold: ValidationFold, timestamp_utc_msc: int):
    from .enums import FoldRole
    if fold.train.contains(timestamp_utc_msc): return FoldRole.TRAIN
    if fold.purge_before_validation and fold.purge_before_validation.contains(timestamp_utc_msc): return FoldRole.PURGED
    if fold.validation.contains(timestamp_utc_msc): return FoldRole.VALIDATION
    if fold.embargo_before_test and fold.embargo_before_test.contains(timestamp_utc_msc): return FoldRole.EMBARGO
    if fold.test.contains(timestamp_utc_msc): return FoldRole.TEST
    return None
