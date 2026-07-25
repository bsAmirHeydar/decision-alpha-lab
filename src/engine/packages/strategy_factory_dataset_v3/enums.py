from __future__ import annotations
from enum import Enum

class TradeSide(str, Enum):
    LONG="long"; SHORT="short"
class EntryStyle(str, Enum):
    MARKET="market"; LIMIT="limit"; STOP="stop"
class OutcomeState(str, Enum):
    REJECTED="rejected"; UNFILLED="unfilled"; OPEN="open"; RESOLVED="resolved"; CENSORED="censored"; UNRESOLVED="unresolved"
class TerminalReason(str, Enum):
    NONE="none"; STOP="stop"; TARGET="target"; TRAIL="trail"; TIME="time"; END_OF_PATH="end_of_path"; ENTRY_EXPIRED="entry_expired"; REJECTED="rejected"; DATA_GAP="data_gap"
class TaskKind(str, Enum):
    BINARY="binary"; REGRESSION="regression"; RANKING="ranking"; TREATMENT_CHOICE="treatment_choice"; SURVIVAL="survival"; COMPETING_RISK="competing_risk"; QUANTILE="quantile"; MULTI_TASK="multi_task"; NOVELTY="novelty"; BOUNDED_POLICY="bounded_policy"
class CensoringKind(str, Enum):
    NONE="none"; RIGHT="right"; INTERVAL="interval"; COMPETING="competing"; UNRESOLVED="unresolved"
class FoldRole(str, Enum):
    TRAIN="train"; CALIBRATION="calibration"; VALIDATION="validation"; TEST="test"; EMBARGO="embargo"; PURGED="purged"; UNUSED="unused"
class TransformKind(str, Enum):
    IDENTITY="identity"; STANDARDIZE="standardize"; ROBUST_SCALE="robust_scale"; MINMAX="minmax"; IMPUTE_MEDIAN="impute_median"; MISSINGNESS_MASK="missingness_mask"; CLIP="clip"
class LeakageSeverity(str, Enum):
    INFO="info"; WARNING="warning"; ERROR="error"; FATAL="fatal"
class UtilityDirection(str, Enum):
    MAXIMIZE="maximize"; MINIMIZE="minimize"
class LabelMaturityPolicy(str, Enum):
    REQUIRE_RESOLVED="require_resolved"; ALLOW_RIGHT_CENSORED="allow_right_censored"; ALLOW_UNFILLED="allow_unfilled"; REQUIRE_ALL_SIBLINGS="require_all_siblings"
