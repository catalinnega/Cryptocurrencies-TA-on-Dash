import dash_app.dash_settings as ds
import pandas as pd
import sqlite3
from ochlv.ochlv_settings import settings as ochlv_settings

def get_ochlv():
    con_ochlv = sqlite3.connect(ochlv_settings['db_path'])
    df_ochlv = pd.read_sql_query(f"select * from {ochlv_settings['table_name']} ORDER BY timestamp DESC LIMIT {ds.QUEUE_LEN}", con_ochlv)
    df_ochlv['timestamp'] = pd.to_datetime(df_ochlv['timestamp'], unit='ms')
    ts_ochlv = df_ochlv.timestamp
    o = df_ochlv.open.values
    h = df_ochlv.high.values
    l = df_ochlv.low.values
    c = df_ochlv.close.values
    v = df_ochlv.volume.values
    return {'ts_ochlv' : ts_ochlv,
            'open' : o,
            'close' : c,
            'high' : h,
            'low' : l,
            'volume' : v
    }