import numpy as np
import my_db

class ADX(my_db.UpdateDB):
    def __init__(self, **kwargs):
        self.table_name = kwargs['table_name'] 
        self.period_size = kwargs['period_size'] 

        self.__tr_win = np.zeros(self.period_size)
        self.__pos_dm_win = np.zeros(self.period_size)
        self.__neg_dm_win = np.zeros(self.period_size)
        self.__adx_win = np.zeros(self.period_size)

        self.ts = 0
        self.prev_close = 0
        self.prev_high = 0
        self.prev_low = 0
        self.pos_dm = 0
        self.neg_dm = 0
        self.pos_di = 0
        self.neg_di = 0
        self.dx = 0

        self.smoothed_tr = 0
        self.smoothed_pos_dm = 0
        self.smoothed_neg_dm = 0
        self.smoothed_adx = 0  

        #self.ceva_cnt = 40 

        self.__init_phase_dx = self.period_size
        self.__init_phase_adx = self.period_size
        self.vals = []
        
        kwargs.update({
        'table_name' : kwargs['table_name'],
        'table_list' :  kwargs['table_list'],
        'update_tdiff' : kwargs['update_tdiff'],
        'replace_last' : False
        })
        super().__init__(self, **kwargs)
    
    def update_latest(self):
        df = super().fetch_latest_data(1)
        if(df is None or len(df.index) == 0):
            return
        self.__init_phase_dx = 0
        self.__init_phase_adx = 0
        self.smoothed_tr = df.tr.values[0]
        self.smoothed_pos_dm = df.pos_dm.values[0]
        self.smoothed_neg_dm = df.neg_dm.values[0]
        self.smoothed_adx = df.adx.values[0]
        
    def reset_bufs(self):
        self.vals = []

    def __get_cirbuf(self, arr, val):
        arr[:-1] = arr[1:]
        arr[-1] = val
        return arr
    
    def __get_window(self):
        self.__pos_dm_win = self.__get_cirbuf(self.__pos_dm_win, self.pos_dm)
        self.__neg_dm_win = self.__get_cirbuf(self.__neg_dm_win, self.neg_dm)
        self.__tr_win = self.__get_cirbuf(self.__tr_win, self.true_range)
        self.__adx_win = self.__get_cirbuf(self.__adx_win, self.dx)

    def compute(self, sample):
        self.true_range = max(sample['high'] - sample['low'],
                        np.abs(sample['high'] - self.prev_close),
                        np.abs(sample['low'] - self.prev_close)
                        )
        self.prev_close = sample['close']
        diff_h = sample['high'] - self.prev_high
        diff_l = self.prev_low - sample['low']
        # diff_h_l = np.abs(diff_h) - np.abs(diff_l)
        self.pos_dm = diff_h if diff_h >= 0 and diff_h > diff_l else 0
        self.neg_dm = diff_l if diff_l > 0 and diff_l > diff_h else 0
        self.prev_high = sample['high']
        self.prev_low = sample['low']

        if(self.__init_phase_dx or self.__init_phase_adx):
            self.__get_window()

        if(self.__init_phase_dx):
            self.__init_phase_dx -= 1
            if(not self.__init_phase_dx):
                self.smoothed_tr = np.sum(self.__tr_win)
                self.smoothed_pos_dm = np.sum(self.__pos_dm_win)
                self.smoothed_neg_dm = np.sum(self.__neg_dm_win)
        else:
            self.smoothed_tr = self.smoothed_tr - (self.smoothed_tr / self.period_size) + self.true_range
            self.smoothed_pos_dm = self.smoothed_pos_dm - (self.smoothed_pos_dm / self.period_size) + self.true_range
            self.smoothed_neg_dm = self.smoothed_neg_dm - (self.smoothed_neg_dm / self.period_size) + self.true_range

            self.pos_di = 100 * self.smoothed_pos_dm / self.smoothed_tr if self.smoothed_tr else 0
            self.neg_di = 100 * self.smoothed_neg_dm / self.smoothed_tr if self.smoothed_tr else 0
            self.dx = 100 * np.abs(self.pos_di - self.neg_di / (self.pos_di + self.neg_di)) if self.pos_di + self.neg_di != 0 else 0
            if(self.__init_phase_adx):
                self.__init_phase_adx -= 1
                if(not self.__init_phase_adx):
                    self.smoothed_adx = np.sum(self.__adx_win)
            else:
                self.smoothed_adx = (self.smoothed_adx * (self.period_size - 1) + self.dx) / self.period_size
        
    def update(self, sample):
        self.ts = int(sample['ts'])
        self.compute(sample)
        self.vals.append([
            self.ts,
            sample['close'],
            self.smoothed_tr,
            self.pos_di,
            self.neg_di,
            self.smoothed_adx,
        ])
        # if(self.ceva_cnt):
        #     a = [
        #     self.ts,
        #     sample['close'],
        #     self.smoothed_tr,
        #     self.pos_di,
        #     self.neg_di,
        #     self.smoothed_adx,
        #     self.dx,
        #     self.smoothed_neg_dm,
        #     self.smoothed_pos_dm,
        #     self.pos_dm,
        #     self.neg_dm
        #     ]
        #     print(f"ceva {a}")
        #     self.ceva_cnt -= 1
        super().update_db(self.vals)
    
    def flush(self):
        if(len(self.vals) == 0):
            super().flush_db(self.vals)
