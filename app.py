import streamlit as st
import pandas as pd

# Backend imports (we will fill these in once you send the files)
# from backend.data_ingestion import load_data
# from backend.data_processing import process_data
# from backend.output_generator import generate_basic_plot
# from backend.nlp_query_engine import parse_query
# from backend.config import DEFAULT_YEAR, DEFAULT_METRIC

st.set_page_config(
    page_title="Delaware County Census Explorer",
    layout="wide"
)

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("Controls")

section = st.sidebar.radio(
    "Choose a section:",
    ["Overview", "Trends", "NLP Q&A", "Download"]
)

# -----------------------------
# Cached data loader
# -----------------------------
@st.cache_data
def get_data():
    # df = load_data()
    # return df
    return pd.DataFrame()  # placeholder until we connect your backend

df = get_data()

# -----------------------------
# Overview Section
# -----------------------------
if section == "Overview":
    st.title("Delaware County Census Overview")

    st.write("Summary metrics will go here.")
    # processed = process_data(df)
    # st.dataframe(processed)

# -----------------------------
# Trends Section
# -----------------------------
elif section == "Trends":
    st.title("Trends Over Time")

    st.write("Trend charts will go here.")
    # fig = generate_basic_plot(df, "year", "population")
    # st.image(fig)

# -----------------------------
# NLP Section
# -----------------------------
elif section == "NLP Q&A":
    st.title("Ask a Question")

    query = st.text_input("Ask something about Delaware County census data")

    if query:
        st.write("Interpreting your question...")
        # intent = parse_query(query)
        # result = handle_intent(intent, df)
        # st.write(result)

# -----------------------------
# Download Section
# -----------------------------
elif section == "Download":
    st.title("Download Data")

    st.write("Download cleaned or raw data.")
    # st.download_button("Download CSV", df.to_csv(index=False), "delco_data.csv")
