import sqlite3
import pandas as pd
import dash_app.dash_settings as ds

import plotly
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots

"""
get_graph()
        - takes the following args:
            ts_ochlv - this is the array of OCHLV timestamps
            o,c,h,l,v - the OCHLV variables
            ts - the indicator timestamps
            **indicator_args - the indicator specific variables. IMPORTANT: the arguments names must be the name as the keys of the returned dict from get_vals() method!!
        - returns a plotly graph obj.
"""
def get_graph(**kwargs):
        ts_ochlv = kwargs['ts_ochlv']
        o = kwargs['open']
        c = kwargs['close']
        h = kwargs['high']
        l = kwargs['low']
        v = kwargs['volume']
        upperline = kwargs['upperline']
        lowerline = kwargs['lowerline']
        squeeze = kwargs['squeeze']
        sma_vals = kwargs['sma']

        data1 = go.Candlestick(
                open=list(o), 
                high=list(h), 
                low=list(l), 
                close=list(c), 
                x=list(ts_ochlv), 
                name="OCHLV", 
                visible=True, 
                )
        data2 = plotly.graph_objs.Scatter(
                x=list(ts_ochlv),
                y=list(upperline),
                name='upperline',
                visible=True,
                marker=dict(color='DarkGreen'),
                )
        data3 = plotly.graph_objs.Scatter(
                x=list(ts_ochlv),
                y=list(lowerline),
                name='lowerline',
                visible=True,
                fill='tonexty',
                marker=dict(color='DarkGreen'),
                )
        data4 = plotly.graph_objs.Scatter(
                x=list(ts_ochlv),
                y=list(sma_vals),
                name='SMA',
                visible=True,
                marker=dict(color='DarkBlue'),
                )
        data5 = plotly.graph_objs.Bar(
                x=list(ts_ochlv),
                y=list(v),
                visible=True,
                name="volume",
                marker=dict(color='Yellow'),
                yaxis='y2'
                )
        data6 = plotly.graph_objs.Scatter(
                x=list(ts_ochlv),
                y=list(squeeze),
                visible=True,
                name="squeeze",
                marker=dict(color='Orange'),
                yaxis='y2'
                )        
        return {
            'data': [data1, data2, data3, data4, data5, data6],
            'layout' : go.Layout(
                            xaxis=dict(range=[min(ts_ochlv),max(ts_ochlv)]),
                            yaxis=dict(range=[min(lowerline) - (min(lowerline) * 8/100), max(upperline) + (max(upperline) * 1/100)]),
                            yaxis2=dict(range=[min(v),max(v)*3.5], title="", overlaying='y', showline=False, showgrid=False, zeroline=False, visible=False),
                            xaxis2=dict(zeroline=False),
                            yaxis_title = "Dollar",
                            xaxis_title = "GMT Time",
                            title="Bollinger Bands", 
                            font={'color': ds.app_colors['text']},
                            plot_bgcolor = ds.app_colors['background'],
                            paper_bgcolor = ds.app_colors['background'],
                            xaxis_rangeslider_visible=False,
                            autosize=False,
                            height=875,
                            )
                }