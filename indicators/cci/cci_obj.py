import numpy as np
import my_db

class CCI(my_db.UpdateDB):
    def __init__(self, **kwargs):
        self.table_name = kwargs['table_name'] 
        self.period_size = kwargs['period_size'] 

        self.__window = np.zeros(self.period_size)

        self.ts = 0
        self.typical_price = 0
        self.cci = 0
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
        h = df.high.values
        l = df.low.values
        typical_price_arr = np.divide(np.add(np.add(c,l),h), 3)
        for i in typical_price_arr:
            self.typical_price = i
            self.__get_window()
        
    def reset_bufs(self):
        self.vals = []
    
    def __get_window(self):
        self.__window[:-1] = self.__window[1:]
        self.__window[-1] = self.typical_price    


    def compute(self, sample):
        self.typical_price = (sample['close'] + sample['low'] + sample['high']) / 3
        self.__get_window()

        sma = np.sum(self.__window) / self.period_size
        mean_deviation = np.sum(np.abs(np.subtract(self.__window, sma))) / self.period_size
        self.cci = (self.typical_price - sma) / (0.015 * mean_deviation)  if(mean_deviation != 0) else 0

    def update(self, sample):
        self.ts = int(sample['ts'])
        self.compute(sample)
        self.vals.append([
            self.ts,
            sample['close'],
            sample['high'],
            sample['low'],
            sample['volume'],
            self.cci
        ])
        super().update_db(self.vals)
    
    def flush(self):
        if(len(self.vals) == 0):
            super().flush_db(self.vals)
