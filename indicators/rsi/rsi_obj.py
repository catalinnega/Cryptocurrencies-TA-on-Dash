import numpy as np
import my_db

class RSI(my_db.UpdateDB):
    def __init__(self, **kwargs):
        self.table_name = kwargs['table_name'] 
        self.period_size = kwargs['period_size'] 

        self.__avg_up = np.zeros(self.period_size)
        self.__avg_down = np.zeros(self.period_size)

        self.ts = 0
        self.prev_close = 0
        self.rsi = 0
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
        self.__window_close = c
        for i in c:
            self.__get_window({'close' : i})
            self.prev_close = i
        
    def reset_bufs(self):
        self.vals = []
    
    def __get_window(self, sample):
        self.__avg_up[:-1] = self.__avg_up[1:]
        self.__avg_down[:-1] = self.__avg_down[1:]
        if sample['close'] > self.prev_close:
            self.__avg_up[-1] = sample['close'] - self.prev_close
            self.__avg_down[-1] = 0
        else:
            self.__avg_down[-1] = self.prev_close - sample['close']
            self.__avg_up[-1] = 0            


    def compute(self, sample):
        self.__get_window(sample)
        avg_up_buf = self.__avg_up
        avg_down_buf = self.__avg_down

        avg_up = np.sum(avg_up_buf) / self.period_size
        avg_down = np.sum(avg_down_buf) / self.period_size
        rs = 0 if avg_down == 0 else avg_up / avg_down 
        self.rsi = 100 - 100 / (1 + rs)


    def update(self, sample):
        self.ts = int(sample['ts'])
        self.compute(sample)
        self.prev_close = sample['close']
        self.vals.append([
            self.ts,\
            self.prev_close,\
            self.rsi
        ])
        super().update_db(self.vals)
    
    def flush(self):
        if(len(self.vals) == 0):
            super().flush_db(self.vals)
