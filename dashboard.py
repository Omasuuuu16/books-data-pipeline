import dash
from dash import dcc, html, dash_table, Input, Output
import plotly.express as px
import duckdb
import pandas as pd

# Connect to DuckDB
con = duckdb.connect(r"C:\Users\Lenovo\depitask\airflow_s4\include\books.duckdb")
df = con.execute("""
    SELECT 
        title,
        rating_number,
        CAST(REGEXP_REPLACE(price_clean::VARCHAR, '[^0-9.]', '', 'g') AS DOUBLE) as price_clean
    FROM fct_books
""").df()
con.close()

app = dash.Dash(__name__)

app.layout = html.Div(style={"fontFamily": "Arial", "padding": "20px", "backgroundColor": "#f9f9f9"}, children=[

    html.H1("📚 Books Dashboard", style={"textAlign": "center", "color": "#2c3e50"}),

    # Filter
    html.Div([
        html.Label("Filter by Rating:"),
        dcc.Dropdown(
            id="rating-filter",
            options=[{"label": "All", "value": "All"}] + 
                    [{"label": str(i), "value": i} for i in sorted(df["rating_number"].unique())],
            value="All",
            clearable=False,
            style={"width": "300px"}
        )
    ], style={"marginBottom": "20px"}),

    # Bar chart
    dcc.Graph(id="rating-chart"),

    # Table
    dash_table.DataTable(
        id="books-table",
        columns=[{"name": col, "id": col} for col in df.columns],
        page_size=15,
        style_table={"overflowX": "auto"},
        style_header={"backgroundColor": "#2c3e50", "color": "white", "fontWeight": "bold"},
        style_cell={"textAlign": "left", "padding": "8px"},
        style_data_conditional=[
            {"if": {"row_index": "odd"}, "backgroundColor": "#f2f2f2"}
        ]
    )
])

@app.callback(
    Output("rating-chart", "figure"),
    Output("books-table", "data"),
    Input("rating-filter", "value")
)
def update(rating):
    filtered = df if rating == "All" else df[df["rating_number"] == rating]
    
    fig = px.bar(
        filtered.groupby("rating_number").size().reset_index(name="count"),
        x="rating_number",
        y="count",
        title="Number of Books per Rating",
        color="rating_number",
        labels={"rating_number": "Rating", "count": "Number of Books"}
    )

    return fig, filtered.to_dict("records")

if __name__ == "__main__":
    app.run(debug=True)