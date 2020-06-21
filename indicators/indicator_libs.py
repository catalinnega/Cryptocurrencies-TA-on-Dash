import dash_app.bb as bb
import dash_app.ikh as ikh
import dash_app.rsi as rsi
import dash_app.sma as sma
import dash_app.ema as ema
import dash_app.macd as macd
import dash_app.mfi as mfi
import dash_app.atr as atr
import dash_app.cci as cci
import dash_app.cmf as cmf
import dash_app.nlms as nlms
import dash_app.snr as snr
import dash_app.adx as adx

from indicators.adx.adx_settings import settings as adx_settings
from indicators.atr.atr_settings import settings as atr_settings
from indicators.bb.bb_settings import settings as bb_settings
from indicators.cci.cci_settings import settings as cci_settings
from indicators.cmf.cmf_settings import settings as cmf_settings
from indicators.ema.ema_settings import settings as ema_settings
from indicators.ikh.ikh_settings import settings as ikh_settings
from indicators.macd.macd_settings import settings as macd_settings
from indicators.mfi.mfi_settings import settings as mfi_settings
from indicators.nlms.nlms_settings import settings as nlms_settings
from indicators.rsi.rsi_settings import settings as rsi_settings
from indicators.sma.sma_settings import settings as sma_settings
from indicators.snr.snr_settings import settings as snr_settings


from indicators.adx.adx_obj import ADX
from indicators.atr.atr_obj import ATR
from indicators.bb.bb_obj import BB
from indicators.cci.cci_obj import CCI
from indicators.cmf.cmf_obj import CMF
from indicators.ema.ema_obj import EMA
from indicators.ikh.ikh_obj import IKH
from indicators.macd.macd_obj import MACD
from indicators.mfi.mfi_obj import MFI
from indicators.nlms.nlms_obj import NLMS
from indicators.rsi.rsi_obj import RSI
from indicators.sma.sma_obj import SMA
from indicators.snr.snr_obj import SNR

import os
root_path = os.getcwd()

indicators_list = [
    {'name':"Bollinger Bands",                          "id":"BB", "dash_lib":bb, "settings":bb_settings, "obj":BB, "proc":[]},
    {'name':"Ichimoku Cloud",                           "id":"IKH", "dash_lib":ikh, "settings":ikh_settings, "obj":IKH, "proc":[]},
    {'name':"Relative Strength Index",                  "id":"RSI", "dash_lib":rsi, "settings":rsi_settings, "obj":RSI, "proc":[]},
    {'name':"Simple Moving Average",                    "id":"SMA", "dash_lib":sma, "settings":sma_settings, "obj":SMA, "proc":[]},
    {'name':"Exponential moving average",               "id":"EMA", "dash_lib":ema, "settings":ema_settings, "obj":EMA, "proc":[]},
    {'name':"Moving Average Convergence Divergence",    "id":"MACD", "dash_lib":macd, "settings":macd_settings, "obj":MACD, "proc":[]},
    {'name':"Money Flow Index",                         "id":"MFI", "dash_lib":mfi, "settings":mfi_settings, "obj":MFI, "proc":[]},
    {'name':"Average True Range",                       "id":"ATR", "dash_lib":atr, "settings":atr_settings, "obj":ATR, "proc":[]},
    {'name':"Commodity Channel Index",                  "id":"CCI", "dash_lib":cci, "settings":cci_settings, "obj":CCI, "proc":[]},
    {'name':"Chaikin Money Flow",                       "id":"CMF", "dash_lib":cmf, "settings":cmf_settings, "obj":CMF, "proc":[]},
    {'name':"Normalized Least Mean Squares",            "id":"NLMS", "dash_lib":nlms, "settings":nlms_settings, "obj":NLMS, "proc":[]},
    {'name':"Noise/Signal Estimator",                   "id":"SNR", "dash_lib":snr, "settings":snr_settings, "obj":SNR, "proc":[]},
    {'name':"Average Directional Index",                "id":"ADX", "dash_lib":adx, "settings":adx_settings, "obj":ADX, "proc":[]}
]
