import indicators.rsi.rsi_settings as rsi_settings
from indicators.rsi.rsi_obj import RSI
import ochlv_db.db_settings as db_settings
import sqlite3
import pandas as pd
from tqdm import tqdm
import time
from datetime import datetime

stop_streaming = False

def rsi_fn(n = '-------rsi_idle-------'):
    kwargs = {
        'path': rsi_settings.db_path, 
        'table_name': rsi_settings.table_name,
        'table_list': rsi_settings.table_list,
        'update_tdiff': rsi_settings.update_tdiff,
        }
    kwargs.update(rsi_settings.settings)
    rsi = RSI(**kwargs)
    rsi.update_latest()
    while stop_streaming == False:
        print(n)
    
        last_ts = rsi.get_latest_time(None, rsi_settings.table_name, "TIMESTAMP")
        if(last_ts is None): last_ts = 0

        con_ochlv = sqlite3.connect(db_settings.db_path)
        df = pd.read_sql_query(f"SELECT TIMESTAMP, close from Bitfinex_OCHLV_15m WHERE TIMESTAMP >= {last_ts}", con_ochlv)
        c = df.close.values
        ts_vals = df.TIMESTAMP.values
        if(len(ts_vals) > 0):
            for i in tqdm(range(len(c))):
                if(ts_vals[i] > last_ts):
                    sample = {
                        'close': c[i]
                    }
                    rsi.update(ts_vals[i], sample)
            rsi.flush()
            print(n, f"Finished update. Last at {datetime.utcfromtimestamp(ts_vals[-1]/1000).strftime('%Y-%m-%d %H:%M:%S')} local datetime.")
        time.sleep(1 * 60)
