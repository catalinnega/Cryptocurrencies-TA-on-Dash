import numpy as np
import my_db

class VAR_LB(my_db.UpdateDB):
    def __init__(self, **kwargs):
        self.table_name = kwargs['table_name'] 
        self.apriori_wlen = kwargs['apriori_wlen'] 
        self.apost_wlen = kwargs['aposteriori_wlen'] 
        self.var_ratio = kwargs['var_ratio'] 

        self.__apriori_window = np.zeros(self.apriori_wlen)
        self.__aposteriori_window = np.zeros(self.apost_wlen)
        self.__prev_var_window = np.zeros(self.apost_wlen)
        self.__prev_label_window = np.multiply(np.ones(self.apost_wlen), -1)

        self.ts = 0
        self.apriori_var = 0
        self.aposteriori_mean = 0
        self.prev_close = 0
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
    
    def __get_cirbuf(self, arr, val):
        arr[:-1] = arr[1:]
        arr[-1] = val
        return arr

    def __get_window(self, sample):
        self.__get_cirbuf(self.__apriori_window, self.change_ratio)
        self.__get_cirbuf(self.__aposteriori_window, sample['close']) 

    def compute(self, sample):
        self.change_ratio = (sample['close'] - self.prev_close) / sample['close'] if sample['close'] else 0
        self.__get_window(sample)

        self.apriori_var = np.sqrt(np.var(self.__apriori_window)) * self.var_ratio
        self.__get_cirbuf(self.__prev_var_window, self.apriori_var) 

        apost_close = self.__aposteriori_window[0]
        self.aposteriori_mean = (np.mean(self.__aposteriori_window) - apost_close) / apost_close if apost_close else 0
        self.prev_close = sample['close']

        apriori_var = self.__prev_var_window[0]
        label = 1 if self.aposteriori_mean >= apriori_var and apriori_var else -1
        self.__get_cirbuf(self.__prev_label_window, label)
        self.label = self.__prev_label_window[0]

    def update(self, sample):
        self.ts = int(sample['ts'])
        self.compute(sample)
        self.vals.append([
            self.ts,
            sample['close'],
            self.apriori_var,
            self.aposteriori_mean,
            self.label
        ])
        super().update_db(self.vals)
    
    def flush(self):
        if(len(self.vals) == 0):
            super().flush_db(self.vals)
