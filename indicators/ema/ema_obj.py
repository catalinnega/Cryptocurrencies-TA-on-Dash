import numpy as np
import my_db

class EMA(my_db.UpdateDB):
    def __init__(self, **kwargs):
        self.table_name = kwargs['table_name'] 
        self.period_size = kwargs['period_size'] 

        self.__window = np.zeros(self.period_size)

        self.ts = 0
        self.close = 0
        self.ema = 0
        self.multiplier = 0
        self.__initial_ema_counter = self.period_size
        self.vals = []

        kwargs.update({
        'table_name' : kwargs['table_name'],
        'table_list' :  kwargs['table_list'],
        'update_tdiff' : kwargs['update_tdiff'],
        'replace_last' : False
        })
        super().__init__(self, **kwargs)
    
    def update_latest(self):
        df = super().fetch_latest_data(self.period_size)
        if(df is None or len(df.index) == 0):
            return
        self.__initial_ema_counter = 0
        self.ema = df.ema.values[-1]
        
    def reset_bufs(self):
        self.vals = []
    
    def __get_window(self, sample):
        self.__window[:-1] = self.__window[1:]
        self.__window[-1] = sample['close']        


    def compute(self, sample):
        if(self.__initial_ema_counter > 0):
            self.__initial_ema_counter -= 1
            self.__get_window(sample)
            self.multiplier = 0
            if(self.__initial_ema_counter == 0):
                self.multiplier = 2 / (self.period_size + 1)
                self.ema = np.sum(self.__window) / self.period_size
        self.ema = (sample['close'] - self.ema) * self.multiplier + self.ema     

    def update(self, sample):
        self.ts = int(sample['ts'])
        self.compute(sample)
        self.close = sample['close']
        self.vals.append([
            self.ts,\
            self.close,\
            self.ema
        ])
        super().update_db(self.vals)
    
    def flush(self):
        if(len(self.vals) == 0):
            super().flush_db(self.vals)
