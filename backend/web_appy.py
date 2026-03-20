from flask import Flask, request, render_template_string
from nlp_query_engine import parse_query, map_intents_to_columns, generate_insight
from data_ingestion import fetch_census_api
from data_processing import clean_dataframe, subset_columns

app = Flask(__name__)

HTML_TEMPLATE = """
<!doctype html>
<title>Delaware County Census AI</title>
<h1>Delaware County Census Explorer</h1>
<form method="post">
  <input type="text" name="query" style="width:400px" placeholder="e.g., population by age in Delaware County 2020">
  <input type="submit" value="Search">
</form>
{% if insight %}
  <h2>Insight</h2>
  <p>{{ insight }}</p>
{% endif %}
{% if table_html %}
  <h2>Data</h2>
  {{ table_html|safe }}
{% endif %}
"""

@app.route("/", methods=["GET", "POST"])
def index():
    insight = None
    table_html = None

    if request.method == "POST":
        query = request.form.get("query", "")
        parsed = parse_query(query)
        intents = parsed["intents"]
        year = parsed["year"]

        # Example: fetch a small set of variables; adapt to your needs
        variables = ["NAME", "B01001_001E", "B19013_001E"]
        df = fetch_census_api(year=year, dataset="acs/acs5", variables=variables)
        df = clean_dataframe(df)

        # Map intents to columns
        cols = map_intents_to_columns(intents)
        df_sub = subset_columns(df, cols)
        insight = generate_insight(df_sub, intents)
        table_html = df_sub.to_html(index=False)

    return render_template_string(HTML_TEMPLATE, insight=insight, table_html=table_html)

if __name__ == "__main__":
    app.run(debug=True)
