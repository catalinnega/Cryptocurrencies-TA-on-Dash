import sqlite3
import pandas as pd
import dash_app.dash_settings as ds

import plotly
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots

from indicators.indicator_settings import global_settings
import numpy as np
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
        conversion_line = kwargs['conversion_line']
        base_line = kwargs['base_line']
        none_arr = [None for _ in range(global_settings['IKH']['wlen_displacement'])]
        leading_span_A = kwargs['leading_span_A'][global_settings['IKH']['wlen_displacement']:]
        leading_span_A.extend(none_arr)
        leading_span_B = kwargs['leading_span_B'][global_settings['IKH']['wlen_displacement']:]
        leading_span_B.extend(none_arr)
        displacement = none_arr
        displacement.extend(c[:-global_settings['IKH']['wlen_displacement']])
        print(len(conversion_line), len(leading_span_A), leading_span_A[0], leading_span_A[-1])
# a = [1,2,3]
# a.extend([3,4])
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
                y=list(conversion_line),
                name='conversion line',
                visible=True,
                marker=dict(color='#8470FF'),
                )
        data3 = plotly.graph_objs.Scatter(
                x=list(ts_ochlv),
                y=list(base_line),
                name='base line',
                visible=True,
                marker=dict(color='#FA8072'),
                )
        data4 = plotly.graph_objs.Scatter(
                x=list(ts_ochlv),
                y=list(leading_span_A),
                name='leading span A',
                yaxis='y2',
                visible=True,
                marker=dict(color='#548B54'),
                )
        data5 = plotly.graph_objs.Scatter(
                x=list(ts_ochlv),
                y=list(leading_span_B),
                name='leading span B',
                fill='tonexty',
                yaxis='y2',
                visible=True,
                marker=dict(color='#EE0000'),
                )
        data6 = plotly.graph_objs.Scatter(
                x=list(ts_ochlv),
                y=list(displacement),
                name='displacement',
                visible=True,
                marker=dict(color='#008000'),
                )
        # data7 = plotly.graph_objs.Bar(
        #         x=list(ts_ochlv),
        #         y=list(v),
        #         visible=True,
        #         name="volume",
        #         marker=dict(color='#F4A460'),
        #         yaxis='y2'
        #         )     
        return {
            'data': [data1, data2, data3, data4, data5, data6],
            'layout' : go.Layout(
                            xaxis=dict(range=[min(ts_ochlv),max(ts_ochlv)]),
                            yaxis=dict(range=[min(l) - (min(l) * 8/100), max(h) + (max(h) * 1/100)]),
                            yaxis2=dict(range=[min(l) - (min(l) * 8/100), max(h) + (max(h) * 1/100)], title="", overlaying='y', showline=False, showgrid=False, zeroline=False, visible=False),
                           # yaxis2=dict(range=[min(v),max(v)*3.5], title="", overlaying='y', showline=False, showgrid=False, zeroline=False, visible=False),
                            xaxis2=dict(zeroline=False),
                            yaxis_title = "Dollar",
                            xaxis_title = "GMT Time",
                            title="Ichimoku Cloud", 
                            font={'color': ds.app_colors['text']},
                            plot_bgcolor = ds.app_colors['background'],
                            paper_bgcolor = ds.app_colors['background'],
                            xaxis_rangeslider_visible=False,
                            autosize=False,
                            height=875,
                            )
                }