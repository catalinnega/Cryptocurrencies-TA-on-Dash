import dash
from dash.dependencies import Output, Input, State
import dash_core_components as dcc
import dash_html_components as html
from time import time

import dash_app.dash_settings as ds
import dash_app.ochlv as ochlv
import dash_app.getters as getters
import dash_app.idle as idle
from indicators.indicator_libs import indicators_list

app = dash.Dash(__name__)
app.layout = html.Div(
    [
        html.Div(
        [
            html.H1('Hai, c-a luat-o!', style={'color':"DarkRed", 'textAlign':'center', 'justify':'center'}),

            dcc.Dropdown(
                id='dropdown_input',
                options = getters.get_labels(),
                placeholder="Select an indicator here",
                style={ 'backgroundColor': 'White', 'width' : 250}
            ),
            
            dcc.RadioItems(
                options=ds.radio_options,
                id='radio_input',
                value='15min',
                labelStyle={'color' : ds.app_colors['text'], 'backgroundColor': ds.app_colors['background'],}
            ) ,
            dcc.Graph(id='app_main', config=dict(editable=True)),
            dcc.Interval(
                id='graph-update',
                interval=60*1000, ## ms
            )
        ], style={'backgroundColor': ds.app_colors['background'], 'margin-top':'-20px', 'margin-left':'-10px', 'margin-right':'-10px'}
        ),
    ], style={'backgroundColor': ds.app_colors['background'], 'margin-top':'-20px', 'margin-left':'-0px', 'margin-right':'-0px'},
)

@app.callback(Output('app_main', 'figure'),
              [Input('dropdown_input', 'value'), Input('radio_input', 'value'), Input('graph-update', 'n_intervals')],
              [State('app_main', 'figure')])
def update_graph(dropdown_input, radio_input, n, existing_state):
    ochlv_vals = ochlv.get_ochlv()
    for indicator in indicators_list:
        if(dropdown_input == indicator["id"]):
            indicator_vals = getters.get_vals(indicator["id"])

            comparison = ochlv_vals["ts_ochlv"] == indicator_vals["timestamp"]
            equal_arrays = comparison.all()
            if(equal_arrays == False): 
                print(f"Invalid timestamps. Last OCHLV candle at {ochlv_vals['ts_ochlv'][0]}. Last indicator sample at {indicator_vals['timestamp'][0]}. Try updating DB by running update.py..")
                return existing_state

            fig_args = {}
            fig_args.update(ochlv_vals)
            fig_args.update(indicator_vals)
            fig = indicator["dash_lib"].get_graph(**fig_args)
            return fig

    return idle.get_graph(**ochlv_vals)

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8120 ,debug=True)