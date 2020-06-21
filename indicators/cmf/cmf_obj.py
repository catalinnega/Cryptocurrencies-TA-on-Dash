import numpy as np
import my_db

class CMF(my_db.UpdateDB):
    def __init__(self, **kwargs):
        self.table_name = kwargs['table_name'] 
        self.period_size = kwargs['period_size'] 

        self.__window_mfv = np.zeros(self.period_size)
        self.__window_volume = np.zeros(self.period_size)

        self.ts = 0
        self.cci = 0
        self.money_flow_volume = 0
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
            h_l = h[i] - l[i]
            multiplier = (((c[i] - l[i]) - (h[i] - l[i])) / h_l) if h_l != 0 else 0
            self.money_flow_volume = multiplier * v[i]
            self.__get_window({'volume' : v[i]})
        
    def reset_bufs(self):
        self.vals = []
    
    def __get_window(self, sample):
        self.__window_mfv[:-1] = self.__window_mfv[1:]
        self.__window_mfv[-1] = self.money_flow_volume  

        self.__window_volume[:-1] = self.__window_volume[1:]
        self.__window_volume[-1] = sample['volume']    


    def compute(self, sample):
        h_l = sample['high'] - sample['low']
        if(h_l != 0):
            multiplier = ((sample['close'] - sample['low']) - (sample['high'] - sample['close'])) / h_l
        else:
            multiplier = 0
        self.money_flow_volume = multiplier * sample['volume']
        self.__get_window(sample)

        sum_volume = np.sum(self.__window_volume)
        self.cmf = np.sum(self.__window_mfv) / sum_volume if sum_volume != 0 else 0

    def update(self, sample):
        self.ts = int(sample['ts'])
        self.compute(sample)
        self.vals.append([
            self.ts,
            sample['close'],
            sample['high'],
            sample['low'],
            sample['volume'],
            self.cmf
        ])
        super().update_db(self.vals)
    
    def flush(self):
        if(len(self.vals) == 0):
            super().flush_db(self.vals)
