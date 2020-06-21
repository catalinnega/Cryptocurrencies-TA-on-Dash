import numpy as np
import my_db


class IKH(my_db.UpdateDB):
    def __init__(self, **kwargs):
        self.wlen_conversion_line =  kwargs['wlen_conversion_line']
        self.wlen_base_line = kwargs['wlen_base_line']
        self.wlen_leading_span2 = kwargs['wlen_leading_span2']
        self.wlen_displacement = kwargs['wlen_displacement']
        self.table_name = kwargs['table_name'] 

        self.__maxlen_cirbuf = max(self.wlen_conversion_line, self.wlen_base_line, self.wlen_leading_span2, self.wlen_displacement)
        self.__window_close = np.zeros(self.__maxlen_cirbuf)

        self.ts = 0
        self.conversion_line = 0
        self.base_line = 0
        self.leading_span_A = 0
        self.leading_span_B = 0

        self.close = 0
        self.vals = []


        kwargs.update({
        'table_name' : kwargs['table_name'],
        'table_list' :  kwargs['table_list'],
        'update_tdiff' : kwargs['update_tdiff'],
        'replace_last' : False
        })
        super().__init__(self, **kwargs)
    
    def update_latest(self):
        df = super().fetch_latest_data(self.__maxlen_cirbuf)
        if(df is None or len(df.index) == 0):
            return
        c = df.close.values
        self.__window_close = c
        
    def reset_bufs(self):
        self.vals = []
    
    def __get_window(self, sample):
        self.__window_close[:-1] = self.__window_close[1:]
        self.__window_close[-1] = sample['close']

    def compute(self, sample):
        self.__get_window(sample)
        window_close = self.__window_close

        self.conversion_line = (np.max(window_close[-self.wlen_conversion_line:]) + np.min(window_close[-self.wlen_conversion_line:])) / 2
        self.base_line = (np.max(window_close[-self.wlen_base_line:]) + np.min(window_close[-self.wlen_base_line:])) / 2
        self.leading_span_A = (self.conversion_line + self.base_line) / 2
        self.leading_span_B = (np.max(window_close[-self.wlen_leading_span2:]) + np.min(window_close[-self.wlen_leading_span2:])) / 2

    def update(self, sample):
        self.ts = int(sample['ts'])
        self.compute(sample)
        self.close = sample['close']
        self.vals.append([
            self.ts,
            self.close,
            self.conversion_line,
            self.base_line,
            self.leading_span_A,
            self.leading_span_B,
        ])
        super().update_db(self.vals)
    
    def flush(self):
        if(len(self.vals) == 0):
            super().flush_db(self.vals)

    
    def flush(self):
        if(len(self.vals) == 0):
            super().flush_db(self.vals)
