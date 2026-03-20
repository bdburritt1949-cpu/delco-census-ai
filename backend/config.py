import os
from dotenv import load_dotenv

load_dotenv()

# Example: you can store API keys or base URLs here
CENSUS_API_KEY = os.getenv("CENSUS_API_KEY", "")
CENSUS_BASE_URL = "https://api.census.gov/data"

# Default geography for Delaware County, PA
DELAWARE_COUNTY_FIPS = {
    "state": "42",   # Pennsylvania
    "county": "045", # Delaware County
}

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
RAW_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")

os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)
