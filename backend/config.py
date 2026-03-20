import os
from dotenv import load_dotenv

load_dotenv()

# -------------------------------
# PATHS
# -------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
RAW_DIR = os.path.join(BASE_DIR, "raw")

CENSUS_DATA_PATH = os.path.join(DATA_DIR, "delco_census.csv")

# -------------------------------
# API KEYS
# -------------------------------
CENSUS_API_KEY = os.getenv("CENSUS_API_KEY")

# -------------------------------
# FIPS CODES
# -------------------------------
DELAWARE_COUNTY_FIPS = {
    "state": "42",
    "county": "045"
}

# -------------------------------
# API BASE URL
# -------------------------------
CENSUS_BASE_URL = "https://api.census.gov/data"

# -------------------------------
# APP SETTINGS
# -------------------------------
DEFAULT_YEAR = 2020
DEFAULT_METRIC = "population"
DEFAULT_COUNTY = "Delaware County"
