# Based on https://dash-bootstrap-components.opensource.faculty.ai/examples/iris/

import dash_express as dx
import plotly.express as px
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import dash


# Load data
df = px.data.iris()
feature_cols = [col for col in df.columns if "species" not in col]
feature_labels = [col.replace("_", " ").title() + " (cm)" for col in feature_cols]
feature_options = [
    {"label": label, "value": col} for col, label in zip(feature_cols, feature_labels)
]

# Build app
app = dash.Dash(__name__)

# Use interact to create components
@dx.interact(
    dx.layouts.dbc.DbcSidebarLayout(app, title="Iris Features")
)
def iris(
        x=dbc.Select(id="x-variable", options=feature_options, value="sepal_length"),
        y=dbc.Select(id="y-variable", options=feature_options, value="sepal_width")
):
    return dcc.Graph(
        figure=px.scatter(df, x=x, y=y, color="species"),
    )


app.layout = iris.layout()


# make sure that x and y values can't be the same variable
def filter_options(v):
    """Disable option ability to plot x vs x"""
    return [
        {"label": label, "value": col, "disabled": col == v}
        for col, label in zip(feature_cols, feature_labels)
    ]

# functionality is the same for both dropdowns, so we reuse filter_options
app.callback(Output("x-variable", "options"), [Input("y-variable", "value")])(
    filter_options
)

app.callback(Output("y-variable", "options"), [Input("x-variable", "value")])(
    filter_options
)


if __name__ == "__main__":
    app.run_server(debug=True, port=9007)