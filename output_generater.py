import os
from typing import Optional
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from config import PROCESSED_DIR

def export_table(df: pd.DataFrame, name: str, fmt: str = "csv") -> str:
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    base = os.path.join(PROCESSED_DIR, name)

    if fmt == "csv":
        path = base + ".csv"
        df.to_csv(path, index=False)
    elif fmt in ["xlsx", "excel"]:
        path = base + ".xlsx"
        df.to_excel(path, index=False)
    else:
        raise ValueError(f"Unsupported export format: {fmt}")
    return path

def generate_basic_plot(df: pd.DataFrame,
                        x_col: str,
                        y_col: str,
                        title: str,
                        name: str) -> Optional[str]:
    if x_col not in df.columns or y_col not in df.columns:
        return None

    os.makedirs(PROCESSED_DIR, exist_ok=True)
    path = os.path.join(PROCESSED_DIR, f"{name}.png")

    plt.figure(figsize=(8, 5))
    sns.barplot(data=df, x=x_col, y=y_col)
    plt.title(title)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(path)
    plt.close()
    return path
