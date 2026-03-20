from datetime import datetime
from data_ingestion import fetch_census_api, save_raw
from data_processing import clean_dataframe
from output_generator import export_table

def scheduled_update():
    # Example: update population data yearly
    year = datetime.now().year - 1
    variables = ["NAME", "B01001_001E"]  # total population
    df = fetch_census_api(year=year, dataset="acs/acs5", variables=variables)
    df_clean = clean_dataframe(df)
    raw_path = save_raw(df_clean, f"population_{year}")
    export_table(df_clean, f"population_{year}", fmt="csv")
    print(f"Updated population data for {year}. Raw: {raw_path}")
