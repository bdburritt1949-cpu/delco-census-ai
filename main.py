import argparse
from nlp_query_engine import parse_query, map_intents_to_columns, generate_insight
from data_ingestion import fetch_census_api, load_local_file, filter_delaware_county
from data_processing import clean_dataframe, subset_columns, summarize_dataframe
from output_generator import export_table, generate_basic_plot

def handle_query(query: str,
                 source: str = "api",
                 local_path: str = None,
                 export_fmt: str = "csv"):
    parsed = parse_query(query)
    intents = parsed["intents"]
    year = parsed["year"]

    if source == "api":
        # Example: fetch a generic set of variables; customize as needed
        variables = ["NAME", "B01001_001E", "B19013_001E", "B01002_001E"]
        df = fetch_census_api(year=year, dataset="acs/acs5", variables=variables)
    else:
        if not local_path:
            raise ValueError("local_path is required when source='local'")
        df = load_local_file(local_path)
        # Optionally filter to Delaware County if the file has state/county columns
        try:
            df = filter_delaware_county(df)
        except Exception:
            pass

    df = clean_dataframe(df)
    cols = map_intents_to_columns(intents)
    df_sub = subset_columns(df, cols)

    summary = summarize_dataframe(df_sub)
    insight = generate_insight(df_sub, intents)

    # Export
    export_name = "delco_query_result"
    export_path = export_table(df_sub, export_name, fmt=export_fmt)

    # Optional visualization: if we have NAME and one numeric column
    plot_path = None
    numeric_cols = df_sub.select_dtypes(include="number").columns.tolist()
    if "NAME" in df_sub.columns and numeric_cols:
        plot_path = generate_basic_plot(
            df_sub,
            x_col="NAME",
            y_col=numeric_cols[0],
            title=f"{numeric_cols[0]} by NAME",
            name="delco_query_plot",
        )

    print("=== QUERY ===")
    print(query)
    print("\n=== PARSED ===")
    print(parsed)
    print("\n=== SUMMARY ===")
    print(summary)
    print("\n=== INSIGHT ===")
    print(insight)
    print(f"\nData exported to: {export_path}")
    if plot_path:
        print(f"Plot saved to: {plot_path}")

def main():
    parser = argparse.ArgumentParser(description="Delaware County Census AI Query Tool")
    parser.add_argument("query", type=str, help="Natural language query")
    parser.add_argument("--source", choices=["api", "local"], default="api",
                        help="Data source: 'api' for Census API, 'local' for local file")
    parser.add_argument("--local-path", type=str, default=None,
                        help="Path to local CSV/Excel/JSON file when source='local'")
    parser.add_argument("--export-fmt", choices=["csv", "xlsx"], default="csv",
                        help="Export format for result table")
    args = parser.parse_args()

    handle_query(
        query=args.query,
        source=args.source,
        local_path=args.local_path,
        export_fmt=args.export_fmt,
    )

if __name__ == "__main__":
    main()
