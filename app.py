import streamlit as st
import pandas as pd

# Backend imports
from backend.data_ingestion import (
    load_local_file,
    filter_delaware_county,
    fetch_census_api,
    save_raw_df
)

from backend.config import (
    CENSUS_DATA_PATH,
    DEFAULT_YEAR,
    DEFAULT_METRIC,
    DEFAULT_COUNTY
)

# -----------------------------------
# Streamlit Page Setup
# -----------------------------------
st.set_page_config(
    page_title="Delaware County Census Explorer",
    layout="wide"
)

st.title("Delaware County Census Explorer")

# -----------------------------------
# Cached Data Loader
# -----------------------------------
@st.cache_data
def load_default_data():
    """Loads the default local census CSV."""
    try:
        df = load_local_file(CENSUS_DATA_PATH)
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

df = load_default_data()

# -----------------------------------
# Sidebar Controls
# -----------------------------------
st.sidebar.header("Controls")

section = st.sidebar.radio(
    "Choose a section:",
    ["Overview", "Trends", "Fetch From API", "Download"]
)

# -----------------------------------
# Overview Section
# -----------------------------------
if section == "Overview":
    st.subheader("County Overview")

    if df.empty:
        st.warning("No data loaded.")
    else:
        st.write("Raw Delaware County Census Data:")
        st.dataframe(df)

        st.write("Filtered Delaware County Rows:")
        filtered = filter_delaware_county(df)
        st.dataframe(filtered)

# -----------------------------------
# Trends Section
# -----------------------------------
elif section == "Trends":
    st.subheader("Trends Over Time")

    if df.empty:
        st.warning("No data available for trend analysis.")
    else:
        if "year" in df.columns:
            st.line_chart(df.set_index("year")["population"])
        else:
            st.info("No 'year' column found — cannot plot trends.")

# -----------------------------------
# Fetch From API Section
# -----------------------------------
elif section == "Fetch From API":
    st.subheader("Fetch Census Data From API")

    year = st.number_input("Year", min_value=2000, max_value=2024, value=DEFAULT_YEAR)
    dataset = st.text_input("Dataset (e.g., acs/acs5)", value="acs/acs5")
    variables = st.text_input("Variables (comma-separated)", value="NAME,B01001_001E")

    if st.button("Fetch Data"):
        vars_list = [v.strip() for v in variables.split(",")]

        try:
            api_df = fetch_census_api(
                year=year,
                dataset=dataset,
                variables=vars_list
            )
            st.success("Data fetched successfully!")
            st.dataframe(api_df)

            if st.button("Save to RAW folder"):
                path = save_raw_df(api_df, f"api_{year}")
                st.success(f"Saved to {path}")

        except Exception as e:
            st.error(f"API Error: {e}")

# -----------------------------------
# Download Section
# -----------------------------------
elif section == "Download":
    st.subheader("Download Data")

    if df.empty:
        st.warning("No data available to download.")
    else:
        st.download_button(
            "Download CSV",
            df.to_csv(index=False),
            file_name="delco_census.csv",
            mime="text/csv"
        )
