from typing import Dict, Any, List
import re

# Simple keyword-based intent detection and mapping.
# You can later replace this with a trained model (e.g., scikit-learn or transformers).

INTENT_KEYWORDS = {
    "population": ["population", "people", "residents"],
    "age": ["age", "ages"],
    "income": ["income", "earnings"],
    "housing": ["housing", "households", "homes", "units"],
    "race": ["race", "ethnicity", "demographics"],
}

# Map intents to example column names (adapt to your actual dataset)
INTENT_TO_COLUMNS = {
    "population": ["total_population", "B01001_001E", "NAME"],
    "age": ["median_age", "B01002_001E", "NAME"],
    "income": ["median_household_income", "B19013_001E", "NAME"],
    "housing": ["total_housing_units", "B25001_001E", "NAME"],
    "race": ["white_alone", "black_alone", "asian_alone", "hispanic_or_latino", "NAME"],
}

def detect_intents(query: str) -> List[str]:
    q = query.lower()
    intents = []
    for intent, keywords in INTENT_KEYWORDS.items():
        if any(kw in q for kw in keywords):
            intents.append(intent)
    if not intents:
        intents.append("population")  # default
    return intents

def parse_query(query: str) -> Dict[str, Any]:
    intents = detect_intents(query)

    # Very simple time detection (e.g., "2019", "2020")
    years = re.findall(r"(20[0-9]{2})", query)
    year = int(years[0]) if years else 2023  # default year

    return {
        "intents": intents,
        "year": year,
        "raw_query": query,
    }

def map_intents_to_columns(intents: List[str]) -> List[str]:
    cols = []
    for intent in intents:
        cols.extend(INTENT_TO_COLUMNS.get(intent, []))
    # Deduplicate while preserving order
    seen = set()
    unique = []
    for c in cols:
        if c not in seen:
            seen.add(c)
            unique.append(c)
    return unique

def generate_insight(df, intents: List[str]) -> str:
    if df is None or df.empty:
        return "No data available for the requested query."

    parts = []
    if "population" in intents and "total_population" in df.columns:
        total = df["total_population"].sum()
        parts.append(f"Estimated total population in Delaware County is about {int(total):,}.")

    if "income" in intents and "median_household_income" in df.columns:
        median_income = df["median_household_income"].median()
        parts.append(f"Median household income is roughly ${median_income:,.0f}.")

    if "age" in intents and "median_age" in df.columns:
        median_age = df["median_age"].median()
        parts.append(f"Median age is around {median_age:.1f} years.")

    if not parts:
        parts.append("Data retrieved successfully. Explore the table for more details.")

    return " ".join(parts)
