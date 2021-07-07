import time
from uuid import uuid4
import dash
import dash_html_components as html

import dash_labs as dl
from dash_labs.plugins import CeleryCallbackManager, DiskcacheCachingCallbackManager

launch_uid = uuid4()

# ## Celery on RabbitMQ
# from celery import Celery
# celery_app = Celery(__name__, backend='rpc://', broker='pyamqp://')
# long_callback_manager = CeleryCallbackManager(celery_app)

# ## Celery on Redis
# from celery import Celery
# celery_app = Celery(
#     __name__, broker='redis://localhost:6379/0', backend='redis://localhost:6379/1'
# )
# long_callback_manager = CeleryCallbackManager(celery_app)

# ## Diskcache
import diskcache

cache = diskcache.Cache("./cache")
long_callback_manager = DiskcacheCachingCallbackManager(
    cache,
    cache_by=[lambda: launch_uid],
    expire=60,
)

app = dash.Dash(
    __name__,
    plugins=[
        dl.plugins.FlexibleCallbacks(),
        dl.plugins.HiddenComponents(),
        dl.plugins.LongCallback(long_callback_manager),
    ],
)

app.layout = html.Div(
    [
        html.Div([html.P(id="paragraph_id", children=["Button not clicked"])]),
        html.Button(id="button_id", children="Run Job!"),
        html.Button(id="cancel_button_id", children="Cancel Running Job!"),
    ]
)


@app.long_callback(
    output=(dl.Output("paragraph_id", "children"), dl.Output("button_id", "n_clicks")),
    args=dl.Input("button_id", "n_clicks"),
    running=[
        (dl.Output("button_id", "disabled"), True, False),
        (dl.Output("cancel_button_id", "disabled"), False, True),
    ],
    cancel=[dl.Input("cancel_button_id", "n_clicks")],
)
def callback(n_clicks):
    time.sleep(2.0)
    return [f"Clicked {n_clicks} times"], (n_clicks or 0) % 4


if __name__ == "__main__":
    app.run_server(debug=True)