import streamlit as st
import pandas as pd

from backend.data_ingestion import ...
from backend.data_processing import ...
from backend.output_generator import generate_basic_plot
from backend.nlp_query_engine import ...
from backend.config import ...

st.set_page_config(
    page_title="Delaware County Census AI",
    page_icon="📊",
    layout="wide"
)

# -----------------------------
# Header
# -----------------------------
st.title("📊 Delaware County Census AI")
st.write("Ask natural-language questions about Delaware County census data.")

# -----------------------------
# Query Input
# -----------------------------
query = st.text_input(
    "Enter your question:",
    placeholder="e.g., population by age in Delaware County 2020"
)

source = st.radio(
    "Choose data source:",
    ["Census API", "Local File"],
    horizontal=True
)

local_file = None
if source == "Local File":
    local_file = st.file_uploader("Upload CSV, Excel, or JSON", type=["csv", "xlsx", "xls", "json"])

run_button = st.button("Run Query")

# -----------------------------
# Main Logic
# -----------------------------
if run_button and query.strip():

    with st.spinner("Processing your query..."):
        parsed = parse_query(query)
        intents = parsed["intents"]
        year = parsed["year"]

        st.subheader("🔍 Parsed Query")
        st.json(parsed)

        # -----------------------------
        # Load Data
        # -----------------------------
        if source == "Census API":
            variables = ["NAME", "B01001_001E", "B19013_001E", "B01002_001E"]
            df = fetch_census_api(
                year=year,
                dataset="acs/acs5",
                variables=variables
            )
        else:
            if local_file is None:
                st.error("Please upload a file.")
                st.stop()

            df = load_local_file(local_file)
            try:
                df = filter_delaware_county(df)
            except Exception:
                pass

        df = clean_dataframe(df)

        # -----------------------------
        # Column Selection
        # -----------------------------
        cols = map_intents_to_columns(intents)
        df_sub = subset_columns(df, cols)

        if df_sub.empty:
            st.error("No matching data found for your query.")
            st.stop()

        # -----------------------------
        # Insight
        # -----------------------------
        insight = generate_insight(df_sub, intents)
        st.subheader("💡 Insight")
        st.write(insight)

        # -----------------------------
        # Data Table
        # -----------------------------
        st.subheader("📄 Data Table")
        st.dataframe(df_sub, use_container_width=True)

        # -----------------------------
        # Visualization
        # -----------------------------
        numeric_cols = df_sub.select_dtypes(include="number").columns.tolist()

        if "NAME" in df_sub.columns and numeric_cols:
            st.subheader("📈 Visualization")

            plot_path = generate_basic_plot(
                df_sub,
                x_col="NAME",
                y_col=numeric_cols[0],
                title=f"{numeric_cols[0]} by NAME",
                name="delco_plot"
            )

            if plot_path:
                st.image(plot_path, caption="Generated Chart")

        # -----------------------------
        # Download
        # -----------------------------
        st.subheader("⬇️ Download Results")

        csv_data = df_sub.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download CSV",
            data=csv_data,
            file_name="delco_query_result.csv",
            mime="text/csv"
        )

        excel_data = df_sub.to_excel("temp.xlsx", index=False)
        with open("temp.xlsx", "rb") as f:
            st.download_button(
                label="Download Excel",
                data=f,
                file_name="delco_query_result.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
