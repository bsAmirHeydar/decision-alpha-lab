from __future__ import annotations
from pathlib import Path
import pandas as pd

REQUIRED_COLUMNS=("time","open","high","low","close")

def normalize_bars(value:pd.DataFrame|Path|str)->pd.DataFrame:
    df=pd.read_csv(value) if isinstance(value,(Path,str)) else value.copy()
    time_col="time"
    if time_col not in df.columns:
        for candidate in ("time_utc","datetime","date"):
            if candidate in df.columns:
                time_col=candidate;break
    required={time_col,"open","high","low","close"}
    missing=required-set(df.columns)
    if missing: raise ValueError(f"missing columns: {sorted(missing)}")
    if "volume" not in df.columns: df["volume"]=0
    df=df.rename(columns={time_col:"time"}).copy()
    df["time"]=pd.to_datetime(df["time"],utc=False)
    for col in ("open","high","low","close","volume"):
        df[col]=pd.to_numeric(df[col],errors="coerce")
    df=df.dropna(subset=["time","open","high","low","close"]).sort_values("time")
    # Deliberately preserve the legacy policy: duplicate timestamps keep the last row.
    df=df.drop_duplicates(subset=["time"],keep="last").reset_index(drop=True)
    return df[["time","open","high","low","close","volume"]]

def align_bars(a:pd.DataFrame,b:pd.DataFrame)->tuple[pd.DataFrame,pd.DataFrame]:
    merged=a[["time"]].merge(b[["time"]],on="time",how="inner")
    return (merged.merge(a,on="time",how="left").reset_index(drop=True),
            merged.merge(b,on="time",how="left").reset_index(drop=True))
