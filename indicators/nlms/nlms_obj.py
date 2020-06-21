import numpy as np
import my_db

class NLMS(my_db.UpdateDB):
    def __init__(self, **kwargs):
        self.table_name = kwargs['table_name'] 
        self.period_size = kwargs['period_size'] 
        self.step_size = kwargs['step_size']
        self.norm_constant = kwargs['norm_constant']

        self.__window = np.zeros(self.period_size)
        self.__filter = np.zeros(self.period_size)

        self.ts = 0
        self.filter_output = 0
        self.error = 0
        self.vals = []
        
        kwargs.update({
        'table_name' : kwargs['table_name'],
        'table_list' :  kwargs['table_list'],
        'update_tdiff' : kwargs['update_tdiff'],
        'replace_last' : False
        })
        super().__init__(self, **kwargs)
    
    def update_latest(self):
        ## should have latest filter values. Currently not saving that in DB..
        return

        
    def reset_bufs(self):
        self.vals = []
    
    def __get_window(self, sample):
        self.__window[:-1] = self.__window[1:]
        self.__window[-1] = sample['close']    


    def compute(self, sample):
        self.__get_window(sample)
        l2_norm = np.dot(self.__window.T, self.__window)
        if(l2_norm != 0):
            self.__filter = np.add(
                        self.__filter,
                        self.step_size * self.error * self.__window / (l2_norm + self.norm_constant)
                        )
        self.filter_output = np.dot(self.__filter, (self.__window.T))
        self.error = sample['close'] - self.filter_output
        c_diff = np.abs(sample['close'] - self.__window[-2])
        div = (c_diff - np.abs(self.error)) / c_diff if c_diff else 0
        div = div if div < 1 else 1
        div = div if div > -1 else -1
        self.error_diff = div

    def update(self, sample):
        self.ts = int(sample['ts'])
        self.compute(sample)
        self.vals.append([
            self.ts,
            sample['close'],
            self.error,
            self.filter_output,
            self.error_diff
        ])
        super().update_db(self.vals)
    
    def flush(self):
        if(len(self.vals) == 0):
            super().flush_db(self.vals)
