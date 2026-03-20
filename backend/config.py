import os
from dotenv import load_dotenv

# Load environment variables safely
load_dotenv()

# -----------------------------
# PATHS
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

# Example dataset paths
CENSUS_DATA_PATH = os.path.join(DATA_DIR, "delco_census.csv")

# -----------------------------
# API KEYS
# -----------------------------
CENSUS_API_KEY = os.getenv("CENSUS_API_KEY")

# -----------------------------
# APP SETTINGS
# -----------------------------
DEFAULT_YEAR = 2020
DEFAULT_METRIC = "population"
DEFAULT_COUNTY = "Delaware County"
