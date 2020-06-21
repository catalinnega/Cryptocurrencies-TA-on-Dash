import numpy as np
import my_db

class MFI(my_db.UpdateDB):
    def __init__(self, **kwargs):
        self.table_name = kwargs['table_name'] 
        self.period_size = kwargs['period_size'] 

        self.__avg_up = np.zeros(self.period_size)
        self.__avg_down = np.zeros(self.period_size)

        self.ts = 0
        self.typical_price = 0
        self.prev_typical_price = 0
        self.raw_money_flow = 0
        self.mfi = 0
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
        v = df.volume.values

        for i in range(len(c)):
            self.prev_typical_price = self.typical_price
            self.typical_price = (c[i] + l[i] + h[i]) / 3
            self.raw_money_flow = self.typical_price * v[i]
            self.__get_window()

    def reset_bufs(self):
        self.vals = []
    
    def __get_window(self):
        self.__avg_up[:-1] = self.__avg_up[1:]
        self.__avg_down[:-1] = self.__avg_down[1:]
        if self.typical_price > self.prev_typical_price:
            self.__avg_up[-1] = self.raw_money_flow
            self.__avg_down[-1] = 0
        else:
            self.__avg_down[-1] = self.raw_money_flow
            self.__avg_up[-1] = 0            


    def compute(self, sample):
        self.prev_typical_price = self.typical_price
        self.typical_price = (sample['close'] + sample['low'] + sample['high']) / 3
        self.raw_money_flow = self.typical_price * sample['volume']
        self.__get_window()
        avg_up_buf = self.__avg_up
        avg_down_buf = self.__avg_down

        avg_up = np.sum(avg_up_buf)
        avg_down = np.sum(avg_down_buf)
        mfi_ratio = 0 if avg_down == 0 else avg_up / avg_down 
        self.mfi = 100 - 100 / (1 + mfi_ratio)


    def update(self, sample):
        self.ts = int(sample['ts'])
        self.compute(sample)
        self.prev_close = sample['close']
        self.vals.append([
            self.ts,
            sample['close'],
            sample['high'],
            sample['low'],
            sample['volume'],
            self.mfi
        ])
        super().update_db(self.vals)
    
    def flush(self):
        if(len(self.vals) == 0):
            super().flush_db(self.vals)
