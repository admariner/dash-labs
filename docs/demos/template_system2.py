import dash_express as dx
import dash_html_components as html
import dash

app = dash.Dash(__name__, plugins=[dx.Plugin()])
tp = dx.templates.DbcCard()

@app.callback(
   dx.Output(html.Div(), "children"),
   dx.Input(html.Button(children="Click Me"), "n_clicks", label="Button to click"),
   template=tp
)
def callback(n_clicks):
    return "Clicked {} times".format(n_clicks)

app.layout = tp.layout(app)

if __name__ == "__main__":
    app.run_server(debug=True)
