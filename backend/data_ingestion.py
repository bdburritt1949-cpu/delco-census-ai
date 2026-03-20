import os
import pandas as pd
import requests
from typing import Optional, Dict, List
from backend.config import (
    RAW_DIR,
    DELAWARE_COUNTY_FIPS,
    CENSUS_BASE_URL,
    CENSUS_API_KEY
)
def load_local_file(path: str) -> pd.DataFrame:
    ext = os.path.splitext(path)[1].lower()
    if ext == ".csv":
        return pd.read_csv(path)
    elif ext in [".xls", ".xlsx"]:
        return pd.read_excel(path)
    elif ext == ".json":
        return pd.read_json(path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

def filter_delaware_county(df: pd.DataFrame,
                           state_col: str = "state",
                           county_col: str = "county") -> pd.DataFrame:
    # You can adapt these column names to your actual schema
    state_fips = DELAWARE_COUNTY_FIPS["state"]
    county_fips = DELAWARE_COUNTY_FIPS["county"]
    mask = (df[state_col].astype(str) == state_fips) & (df[county_col].astype(str) == county_fips)
    return df.loc[mask].copy()

def fetch_census_api(
    year: int,
    dataset: str,
    variables: List[str],
    for_geo: str = "county:045",
    in_geo: str = "state:42",
) -> pd.DataFrame:
    """
    Example: ACS5 dataset
    dataset: 'acs/acs5'
    variables: ['NAME', 'B01001_001E']  # total population
    """
    params = {
        "get": ",".join(variables),
        "for": for_geo,
        "in": in_geo,
    }
    if CENSUS_API_KEY:
        params["key"] = CENSUS_API_KEY

    url = f"{CENSUS_BASE_URL}/{year}/{dataset}"
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    data = resp.json()
    cols = data[0]
    rows = data[1:]
    df = pd.DataFrame(rows, columns=cols)
    return df

def save_raw(df: pd.DataFrame, name: str) -> str:
    path = os.path.join(RAW_DIR, f"{name}.csv")
    df.to_csv(path, index=False)
    return path
