import numpy as np
import my_db

class MACD(my_db.UpdateDB):
    def __init__(self, **kwargs):
        self.table_name = kwargs['table_name'] 
        self.slow_period_size = kwargs['slow_period_size']
        self.fast_period_size = kwargs['fast_period_size'] 
        self.signal_period_size = kwargs['signal_period_size'] 

        self.__max_period_size = max(self.slow_period_size, self.fast_period_size, self.signal_period_size)
        self.__ema_window = np.zeros(self.__max_period_size)
        self.__macd_window = np.zeros(self.signal_period_size)

        self.ts = 0
        self.close = 0
        self.fast_ema = 0
        self.slow_ema = 0
        self.signal_line = 0
        self.macd = 0
        self.macd_histogram = 0
        
        self.__fast_multiplier = 0
        self.__slow_multiplier = 0
        self.__signal_multiplier = 0

        self.__initial_fast_sma_counter = self.slow_period_size
        self.__initial_slow_sma_counter = self.fast_period_size
        self.__initial_signal_counter = self.signal_period_size
        self.__global_counter = self.__max_period_size
        
        self.vals = []

        kwargs.update({
        'table_name' : kwargs['table_name'],
        'table_list' :  kwargs['table_list'],
        'update_tdiff' : kwargs['update_tdiff'],
        'replace_last' : False
        })
        super().__init__(self, **kwargs)
    
    def update_latest(self):
        df = super().fetch_latest_data(1)
        if(df is None or len(df.index) == 0):
            return
        self.__initial_ema_counter = 0
        self.slow_ema = df.slow_ema.values
        self.fast_ema = df.fast_ema.values
        self.signal_line = df.signal_line.values
        self.macd = df.macd.values
        self.__global_counter = 0
        self.__fast_multiplier = 2 / ( self.fast_period_size + 1)
        self.__slow_multiplier = 2 / ( self.slow_period_size + 1)
        self.__signal_multiplier = 2 / ( self.signal_period_size + 1)
        
    def reset_bufs(self):
        self.vals = []
    
    def __get_window(self, sample):
        self.__ema_window[:-1] = self.__ema_window[1:]
        self.__ema_window[-1] = sample['close']

        self.__macd_window[:-1] = self.__macd_window[1:]
        self.__macd_window[-1] = self.macd     

    def __get_initial_sma(self, counter, multiplier, period_size, window):
        ema = 0
        if(counter > 0):
            multiplier = 0
            counter -= 1
            if(counter == 0):
                multiplier = 2 / (period_size + 1)
                ema = np.sum(window[-period_size:]) / period_size     
        return counter, multiplier, ema

    def compute(self, sample):
        if(self.__global_counter > 0):
            self.__global_counter -= 1
            self.__get_window(sample)

            self.__initial_fast_sma_counter,\
            self.__fast_multiplier,\
            self.fast_ema      = self.__get_initial_sma(self.__initial_fast_sma_counter,
                                                        self.__fast_multiplier,
                                                        self.fast_period_size,
                                                        self.__ema_window)

            self.__initial_slow_sma_counter,\
            self.__slow_multiplier,\
            self.slow_ema      = self.__get_initial_sma(self.__initial_slow_sma_counter,
                                                        self.__slow_multiplier,
                                                        self.slow_period_size,
                                                        self.__ema_window)

            self.__initial_signal_counter,\
            self.__signal_multiplier,\
            self.signal_line      = self.__get_initial_sma(self.__initial_signal_counter,
                                                           self.__signal_multiplier,
                                                           self.signal_period_size,
                                                           self.__macd_window)

        self.slow_ema = (sample['close'] - self.slow_ema) * self.__slow_multiplier + self.slow_ema
        self.fast_ema = (sample['close'] - self.fast_ema) * self.__fast_multiplier + self.fast_ema
        self.macd = self.fast_ema - self.slow_ema
        self.signal_line = (self.macd - self.signal_line) * self.__signal_multiplier + self.signal_line
        self.macd_histogram = self.macd - self.signal_line   

    def update(self, sample):
        self.ts = int(sample['ts'])
        self.compute(sample)
        self.close = sample['close']
        self.vals.append([
            self.ts,
            self.close,
            self.fast_ema,
            self.slow_ema,
            self.signal_line,
            self.macd,
            self.macd_histogram
        ])
        super().update_db(self.vals)
    
    def flush(self):
        if(len(self.vals) == 0):
            super().flush_db(self.vals)
