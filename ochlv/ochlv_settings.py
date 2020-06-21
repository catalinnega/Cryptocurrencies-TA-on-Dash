import os

candle_period = '15m'
table_name = "OCHLV_" + candle_period
start_time = 1420084800 # 2015-01-01 in seconds
batch_candles_len = 10000 #10000 max len
root_path = os.getcwd()
ochlv_path = root_path + "/ochlv_db.sqlite"
log_path = root_path + "db_log.log"
settings = {
        'candle_period': candle_period,
        'pair': "tBTCUSD",
        'candles_section': "hist",
        'start_time': start_time,
        'batch_candles_len': batch_candles_len,
        'db_path': ochlv_path,
        'db_log_path': log_path,
        'table_name': table_name
}