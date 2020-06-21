import numpy as np
import my_db

class ATR(my_db.UpdateDB):
    def __init__(self, **kwargs):
        self.table_name = kwargs['table_name'] 
        self.period_size = kwargs['period_size'] 

        self.__window = np.zeros(self.period_size)

        self.ts = 0
        self.true_range = 0
        self.multiplier = 0
        self.prev_close = 0
        self.__initial_avg_counter = self.period_size

        self.atr = 0
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

        self.atr = df.atr.values[0]
        self.true_range = df.true_range.values[0]
        self.__initial_avg_counter = 0
        self.multiplier = self.period_size - 1
        
    def reset_bufs(self):
        self.vals = []

    def __get_initial_avg(self, counter, multiplier, period_size, window):
        avg = self.atr
        if(counter > 0):
            multiplier = 0
            counter -= 1
            if(counter == 0):
                multiplier = self.period_size - 1
                avg = np.sum(window) / period_size     
        return counter, multiplier, avg
    
    def __get_window(self):
        self.__window[:-1] = self.__window[1:]
        self.__window[-1] = self.true_range

    def compute(self, sample):
        self.true_range = max(sample['high'] - sample['low'],
                              np.abs(sample['high'] - self.prev_close),
                              np.abs(sample['low'] - self.prev_close)
                              )
        self.__get_window()
        self.__initial_avg_counter, self.multiplier, self.atr = self.__get_initial_avg(self.__initial_avg_counter,
                                                                                  self.multiplier, 
                                                                                  self.period_size, 
                                                                                  self.__window)
        self.atr = (self.atr * self.multiplier + self.true_range) / self.period_size
        self.prev_close = sample['close']

    def update(self, sample):
        self.ts = int(sample['ts'])
        self.compute(sample)
        self.vals.append([
            self.ts,
            sample['close'],
            self.true_range,
            self.atr
        ])
        super().update_db(self.vals)
    
    def flush(self):
        if(len(self.vals) == 0):
            super().flush_db(self.vals)
