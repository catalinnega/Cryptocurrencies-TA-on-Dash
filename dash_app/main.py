import dash
from dash.dependencies import Output, Input, State
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots
from time import time

import dash_app.dash_settings as ds
import dash_app.ochlv as ochlv
import dash_app.getters as get_vals_lib

app = dash.Dash(__name__)
app.layout = html.Div(
    [
        html.Div(
        [
        html.H1('Hai, c-a luat-o!', style={'color':"#CECECE"}),
        # dcc.Input(id='input', value='', type='text', style={'color':"Black", 'backgroundColor':"Grey"}),
        dcc.Dropdown(
            id='dropdown_input',
            options=[
                {'label': 'Bollinger Bands', 'value': 'BB'},
                {'label': 'Ichimoku Cloud', 'value': 'IKH'},
                {'label': 'Relative Strength Index', 'value': 'RSI'},
                {'label': 'Simple Moving Average', 'value': 'SMA'},
                {'label': 'Exponential Moving Average', 'value': 'EMA'},
                {'label': 'Moving Average Convergence Divergence', 'value': 'MACD'},
            ],
            placeholder="Select an indicator here",
        ),
        dcc.Graph(id='app_main', config=dict(editable=True)),
        dcc.Interval(
            id='graph-update',
            interval=10*1000, ## o secunda
            n_intervals=0
        )
        ], style={'backgroundColor': ds.app_colors['background'], 'margin-top':'-20px', 'margin-left':'-10px', 'margin-right':'-10px'}
        ),
    ], style={'backgroundColor': ds.app_colors['background'], 'margin-top':'-20px', 'margin-left':'-0px', 'margin-right':'-0px'},
)

@app.callback(Output('app_main', 'figure'),
              [Input('dropdown_input', 'value')],
              [State('app_main', 'figure')])
def update_graph(input_data, existing_state):
    ochlv_vals = ochlv.get_ochlv()
    for indicator in ds.indicators_list:
        if(input_data == indicator["name"]):
            indicator_vals = get_vals_lib.get_vals(indicator["name"].lower())

            comparison = ochlv_vals["ts_ochlv"] == indicator_vals["ts"]
            equal_arrays = comparison.all()
            if(equal_arrays == False): 
                print("Invalid timestamps")
                return existing_state

            fig_args = {}
            fig_args.update(ochlv_vals)
            fig_args.update(indicator_vals)
            fig = indicator["lib"].get_graph(**fig_args)
            return fig

    return {'data': [],
            'layout' : go.Layout(
                                height=900,
                                plot_bgcolor = ds.app_colors['background'],
                                paper_bgcolor = ds.app_colors['background']
                                )
                } 

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8120 ,debug=True)