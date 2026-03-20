import pandas as pd
from typing import Dict, Any

def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    # Strip whitespace from column names
    df.columns = [c.strip() for c in df.columns]

    # Replace common missing markers
    df.replace(["", "NA", "N/A", "null", None, -666666666], pd.NA, inplace=True)

    # Try to convert numeric-looking columns
    for col in df.columns:
        # Skip obvious non-numeric columns
        if df[col].dtype == object:
            try:
                df[col] = pd.to_numeric(df[col])
            except Exception:
                # leave as is if conversion fails
                pass
    return df

def summarize_dataframe(df: pd.DataFrame) -> Dict[str, Any]:
    summary = {}
    summary["row_count"] = len(df)
    summary["columns"] = list(df.columns)
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    summary["numeric_columns"] = numeric_cols
    summary["describe"] = df[numeric_cols].describe().to_dict() if numeric_cols else {}
    return summary

def subset_columns(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    existing = [c for c in columns if c in df.columns]
    return df[existing].copy()
