import sqlite3
import pandas as pd
import dash_app.dash_settings as ds

import plotly
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots

def get_graph(**kwargs):
        ts_ochlv = kwargs['ts_ochlv']
        o = kwargs['open']
        c = kwargs['close']
        h = kwargs['high']
        l = kwargs['low']
        v = kwargs['volume']
        snr = kwargs['snr']

        fig = make_subplots(
                        rows = 2,
                        cols = 1,
                        vertical_spacing=0.02)

        fig.add_trace(
        go.Candlestick(
                        open=list(o), 
                        high=list(h), 
                        low=list(l), 
                        close=list(c), 
                        x=list(ts_ochlv), 
                        name="OCHLV", 
                        visible=True, 
                        ),
        row = 1, col = 1
        )
        fig.add_trace(
        go.Scatter(
                        x=list(ts_ochlv),
                        y=list(snr),
                        name='NSR',
                        visible=True,
                        marker=dict(color='Red'),
                        yaxis='y2',
                        xaxis='x2'
        ),
        row = 2, col = 1
        )
        fig.update_layout(
                        height=900,
                        yaxis=dict(domain=[0.35, 1]),
                        yaxis2=dict(domain=[0, 0.25]),
                        title_text="Noise Signal Estimator",
                        xaxis_rangeslider_visible=False,
                        font={'color': ds.app_colors['text']},
                        plot_bgcolor = ds.app_colors['background'],
                        paper_bgcolor = ds.app_colors['background'],
                        autosize=False,
                        hovermode = 'x unified',
                        spikedistance = -1,
                        )

        fig.update_yaxes(
                title_text="NSR",
                range=[min(snr), max(snr)], 
                row = 2,
                col = 1,
                showgrid = False,
                showspikes = True,
                spikemode = 'across',
                spikesnap = 'cursor',
                showline = True,
                spikecolor="Red",
                spikethickness = 1,
                )
        fig.update_yaxes(
                title_text="Dollar",
                range=[min(l) - (min(l) * 1/100), max(h) + (max(h) * 1/100)], 
                row = 1,
                col = 1,
                showgrid = False,
                showspikes = True,
                spikemode = 'across',
                spikesnap = 'cursor',
                showline = True,
                spikecolor="Red",
                spikethickness = 1
                )
        fig.update_xaxes(
                title_text = "GMT time",
                range = [min(ts_ochlv),max(ts_ochlv)], 
                row = 2,
                col = 1,
                showgrid = False,
                showspikes = True,
                spikemode = 'across',
                spikesnap = 'cursor',
                showline = True,
                spikecolor="Red",
                spikethickness = 1
                )
        fig.update_xaxes(
                title_text = " ",
                range = [min(ts_ochlv),max(ts_ochlv)], 
                row = 1,
                col = 1,
                showgrid = False,
                showspikes = True,
                visible=True,
                spikemode = 'across',
                spikesnap = 'cursor',
                showline = True,
                spikecolor="Red",
                spikethickness = 1
                )
        return fig