import dash
import dash_express as dx
import plotly.express as px

tips = px.data.tips()
import dash_html_components as html
import dash_core_components as dcc


app = dash.Dash(__name__)
template = dx.templates.DbcSidebar(title="Dash Express App")
# template = dx.templates.DdkSidebar(title="Dash Express App", sidebar_width="400px", show_editor=True)
# template = dx.templates.DccCard(title="Dash Express App")


graph_id = dx.build_component_id(kind="graph")

graph = template.Graph(id=graph_id)

def filter(max_total_bill, tip_range, sex, selectedData):
    # Let parameterize infer output component
    filtered = tips
    print(selectedData)

    if max_total_bill is not None:
        filtered = filtered.query(f"total_bill < {max_total_bill}")

    if tip_range is not None:
        filtered = filtered.query(f"tip >= {tip_range[0]} & tip <= {tip_range[1]}")

    if sex is not None:
        filtered = filtered.query(f"sex == '{sex}'")

    graph_res = template.Graph(id=graph_id, figure=px.scatter(filtered, x="total_bill", y="tip"))
    return [
        "### Filtered tips plot",
        graph_res,
        html.Hr(),
        "### Filtered tips table",
        filtered,
    ]


callback_components = dx.parameterize(
    app,
    filter,
    input=dict(
        max_total_bill=(0, 50.0, 0.25),
        tip_range=dcc.RangeSlider(min=0, max=20, value=(5, 10)),
        sex=["Male", "Female"],
    ),
    output=dict(
        selectedData=(graph, "selectedData")
    ),
    template=template,
    labels={
        "max_total_bill": "Max total bill ($): {value:.2f}",
        "tip_range": lambda v: "Tip range ($): " + (f"{v[0]:.2f} - {v[1]:.2f}" if v else "None"),
        "sex": "Patron Gender",
    },
    optional=["max_total_bill", "max_tip", "sex", "tip_range"]
)

app.layout = callback_components.layout

if __name__ == "__main__":
    app.run_server(debug=True, port=9038)