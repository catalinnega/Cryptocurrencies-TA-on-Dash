from bitfinex import ClientV2
import my_db as my_db
import logger.my_logger as my_logger
from ochlv.ochlv_settings import settings as db_settings
from copy import copy
from datetime import datetime, timezone
import time

UTC_15_MIN_MS = 15 * 60 * 1000
WAIT = 888
VALID = 777
stop_streaming = False

logging = my_logger.init_logger(db_settings['db_log_path'])

class StreamOCHLV(my_db.UpdateDB):
    def __init__(self):
        self.vals = []
        self.timestamp = 0
        self.start_time = 0
        self.end_time = 0
        self.open = 0.0
        self.close = 0.0
        self.high = 0.0
        self.low = 0.0
        self.volume = 0.0
        self.candles = []
        self.bfx_client = ClientV2()
        self.table_name = db_settings['table_name']
        kwargs = {
        'db_path' : db_settings['db_path'],
        'table_name' : self.table_name,
        'table_list' :  (
                         ['timestamp', 'INT', 'NOT NULL'],
                         ['open', 'FLOAT(5,4)', 'NOT NULL'],
                         ['close', 'FLOAT(5,4)', 'NOT NULL'],
                         ['high', 'FLOAT(5,4)', 'NOT NULL'],
                         ['low', 'FLOAT(5,4)', 'NOT NULL'],
                         ['volume', 'FLOAT(5,4)', 'NOT NULL'],
                         ),
        'update_tdiff' : db_settings['batch_candles_len'],
        'replace_last' : False
        }
        super().__init__(self, **kwargs)

    def reset_bufs(self):
        self.vals = []

    def flush(self):
        super().flush_db(self.vals)
    
    def _fill_missing(self):
        for i in range(1,len(self.candles)):
            diff = self.candles[i][0] - self.candles[i-1][0]
            if(diff > UTC_15_MIN_MS):
                missing_filler = copy(self.candles[i-1])
                missing_filler[0] = missing_filler[0] + UTC_15_MIN_MS
                self.candles.insert(i, missing_filler)
                i -= 1

    def _check_time_interval(self):
        UTC_now_milisec = time.time() * 1000
        if(self.start_time > UTC_now_milisec - UTC_15_MIN_MS):
            wait_time_seconds = int((UTC_15_MIN_MS - (UTC_now_milisec - self.start_time)) / 1000)
            log_new_time = datetime.utcfromtimestamp((UTC_now_milisec + wait_time_seconds*1000)/1000).strftime('%Y-%m-%d %H:%M:%S')
            log_last_time = datetime.utcfromtimestamp((self.start_time)/1000).strftime('%Y-%m-%d %H:%M:%S')
            log_curr_time = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
            logging.info(f"Candles up to date.\nLast candle at {log_last_time}.\nWaiting {wait_time_seconds} seconds.\nLocal time is {log_curr_time}.\nWaiting until {log_new_time}")
            time.sleep(wait_time_seconds)
            self.end_time = self.start_time + UTC_15_MIN_MS
            return
        
        if(self.end_time > UTC_now_milisec - UTC_15_MIN_MS):
            self.end_time = UTC_now_milisec - UTC_15_MIN_MS
        return
    
    def _get_candles(self):
        try:
            self.start_time = self.get_latest_time(None, self.table_name, "timestamp")
            if(self.start_time is None):
                logging.warning("Could not retrive latest timestamp")
                self.start_time = db_settings['start_time'] * 1000
            self.start_time += UTC_15_MIN_MS
        except:
            logging.warning("Could not retrive latest timestamp")
            self.start_time = db_settings['start_time'] * 1000
        self.end_time = self.start_time + UTC_15_MIN_MS * 10000
        
        self._check_time_interval()
        self.candles = self.bfx_client.candles(db_settings['candle_period'],
                                                db_settings['pair'], 
                                                db_settings['candles_section'],
                                                limit = db_settings['batch_candles_len'],
                                                start = self.start_time, 
                                                end = self.end_time,
                                                sort = 1
                                                ) #max 10000 
        self._fill_missing()    

    def update(self):
        self._get_candles()
        if(len(self.candles) == 0):
            return
        super().update_db(self.candles, use_accum = False)
        try:
            self.last_candle_ts = super().get_latest_time(None, self.table_name, "timestamp")
        except:
            self.last_candle_ts = self.start_time
            logging.warning("Could not retrive latest timestamp2")
        logging.info(f"UTC From {self.start_time} to {self.end_time}, last {self.last_candle_ts}.")

def stream_OCHLV_fn():
    stream_ochlv_obj = StreamOCHLV();
    while stop_streaming == False:
        stream_ochlv_obj.update()
        time.sleep(5)

def test_other_fn(n):
    while stop_streaming == False:
        print(n)
        time.sleep(5)
