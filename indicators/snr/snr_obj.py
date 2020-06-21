import numpy as np
import my_db

class SNR(my_db.UpdateDB):
    def __init__(self, **kwargs):
        self.table_name = kwargs['table_name'] 
        self.period_size = kwargs['period_size'] 

        self.__window = np.zeros(self.period_size)

        self.ts = 0
        self.filter_output = 0
        self.error = 0
        self.S = 0
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
        M2 = (1 / self.period_size) * np.sum(np.power(self.__window,2))
        self.S = (1 / self.period_size) * np.power(np.dot(self.__window.T, np.tanh(np.multiply(np.sqrt(self.S), np.divide(self.__window,(M2 - 1))))), 2)
        
        if(self.S <= 0.00000000001):
            self.snr = 1
        else:
             self.snr = abs(20 * np.log10(S))

    def update(self, sample):
        self.ts = int(sample['ts'])
        self.compute(sample)
        self.vals.append([
            self.ts,
            sample['close'],
            self.snr,
        ])
        super().update_db(self.vals)
    
    def flush(self):
        if(len(self.vals) == 0):
            super().flush_db(self.vals)
