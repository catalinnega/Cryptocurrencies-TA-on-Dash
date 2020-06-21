import numpy as np
import my_db

class SMA(my_db.UpdateDB):
    def __init__(self, **kwargs):
        self.table_name = kwargs['table_name'] 
        self.period_size = kwargs['period_size'] 

        self.__window = np.zeros(self.period_size)

        self.ts = 0
        self.close = 0
        self.sma = 0
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
        c = df.close.values
        for i in c:
            self.__get_window({'close' : i})
        
    def reset_bufs(self):
        self.vals = []
    
    def __get_window(self, sample):
        self.__window[:-1] = self.__window[1:]
        self.__window[-1] = sample['close']        


    def compute(self, sample):
        self.__get_window(sample)
        window = self.__window

        self.sma = np.sum(window) / self.period_size

    def update(self, sample):
        self.ts = int(sample['ts'])
        self.compute(sample)
        self.close = sample['close']
        self.vals.append([
            self.ts,\
            self.close,\
            self.sma
        ])
        super().update_db(self.vals)
    
    def flush(self):
        if(len(self.vals) == 0):
            super().flush_db(self.vals)
