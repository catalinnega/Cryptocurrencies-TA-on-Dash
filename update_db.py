import multiprocessing
import os
import pandas as pd
import sqlite3
from tqdm import tqdm
import time
from datetime import datetime

from ochlv.ochlv_settings import settings as ochlv_lib
from ochlv.ochlv_db import ochlv_fn
from indicators.indicator_libs import indicators_list

def standard_fn(name, settings_dict, IndicatorObj, ochlv_lib):
    indicator_obj = IndicatorObj(**settings_dict)
    indicator_obj.update_latest()
    stop_streaming = False
    while stop_streaming == False:
        last_ts = indicator_obj.get_latest_time(None, settings_dict['table_name'], "timestamp")
        if(last_ts is None): last_ts = 0

        con_ochlv = sqlite3.connect(ochlv_lib['db_path'])
        df = pd.read_sql_query(f"SELECT timestamp, close, high, low, volume from {ochlv_lib['table_name']} WHERE timestamp > {last_ts}", con_ochlv)
        close_vals = df.close.values
        high_vals = df.high.values
        low_vals = df.low.values
        volume_vals = df.volume.values
        ts_vals = df.timestamp.values
        if(len(ts_vals) > 0):
            for i in tqdm(range(len(close_vals))):
                if(ts_vals[i] > last_ts):
                    indicator_obj.update({'ts': ts_vals[i],
                                          'close': close_vals[i],
                                          'high': high_vals[i],
                                          'low': low_vals[i],
                                          'volume': volume_vals[i]})
            indicator_obj.flush()
            print(f"__{name}__: Finished update. Last sample at {datetime.utcfromtimestamp(ts_vals[-1]/1000).strftime('%Y-%m-%d %H:%M:%S')} local datetime.")
        time.sleep(3)

if __name__ == '__main__':
    p = multiprocessing.Process(target = ochlv_fn)
    p.start()
    for i in range(len(indicators_list)):
        indicators_list[i]['proc'] = multiprocessing.Process(
                                                            target = standard_fn, 
                                                            args=(
                                                                 indicators_list[i]['name'],
                                                                 indicators_list[i]['settings'],
                                                                 indicators_list[i]['obj'],
                                                                 ochlv_lib
                                                                 )
                                    )
        indicators_list[i]['proc'].start()
