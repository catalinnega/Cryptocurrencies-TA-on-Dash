#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 21:55:13 2019

@author: catalin
"""

import numpy as np
import my_db

class BB(my_db.UpdateDB):
    def __init__(self, **kwargs):
        self.wlen =  kwargs['period_size']
        self.n_std = kwargs['n_std']
        self.__cirbuf = np.zeros(self.wlen)
        self.rd_idx = 0
        self.data = 0.0
        self.sma = 0.0
        self.upperline = 0.0
        self.lowerline = 0.0
        self.squeeze = 0.0
        self.vals = []
        kwargs.update({
        'table_name' : kwargs['table_name'],
        'table_list' :  kwargs['table_list'],
        'update_tdiff' : 4096,
        'replace_last' : False
        })
        self.ts = 0
        super().__init__(self, **kwargs)
    
    def update_latest(self):
        df = super().fetch_latest_data(self.wlen)
        if(df is None or len(df.index) == 0):
            return
        samples = df.input.values
        self.__cirbuf = samples
        
    def reset_bufs(self):
        self.vals = []
    
    def __get_cirbuf(self,sample):
        self.__cirbuf[self.rd_idx] = sample
        self.rd_idx = self.rd_idx + 1 if self.rd_idx < self.wlen - 1 else 0

    def compute(self, sample):
        self.__get_cirbuf(sample)
        wlen = self.wlen
        cirbuf = self.__cirbuf
        mean = np.divide(np.sum(cirbuf), wlen)
        std = np.divide(np.sqrt(np.sum(np.power((np.subtract(cirbuf, mean)), 2))), wlen)

        self.data = sample
        self.sma = mean
        self.upperline = mean + np.multiply(self.n_std,std)
        self.lowerline = mean - np.multiply(self.n_std,std)
        self.squeeze = self.upperline - self.lowerline
    
    def update(self, sample):
        self.ts = int(sample['ts'])
        self.compute(sample['close'])
        self.vals.append([
            self.ts,\
            self.data,\
            self.sma,\
            self.upperline,\
            self.lowerline,\
            self.squeeze,\
        ])
        super().update_db(self.vals)
    
    def flush(self):
        if(len(self.vals) == 0):
            super().flush_db(self.vals)

# proc_time_start = datetime.datetime.now()
# path = "/home/catalin/tmp/bb_db.sqlite"
# kwargs = {'wlen':128, 'path': path}
# bb = BollingerBands(**kwargs)

# dataset_directory = '/home/catalin/tmp/bfx.csv'
# data = gd.get_data(dataset_directory)
# c = data['c']
# del data

# from tqdm import tqdm
# for i in tqdm(range(len(c))):
#     bb.update(c[i])
# bb.flush()

# proc_time_end = datetime.datetime.now()
# print('proctime: ', proc_time_end - proc_time_start)

# pc.plot_candles(o,c,h,l,
#     indicators = [[bb.sma, "SMA"],
#      [bb.upperline, "upperline"],
#      [bb.lowerline, "lowerline"]],
#     oscillator = [bb.sma_cross, 'SMA cross'],
#     ylabel = 'btc/usd',
#     xlabel = '15min candles',
#     title = 'Bollinger Bands'
# )

# import pickle
# with open("/home/catalin/tmp/bb_dict.pkl", "wb") as f:
#     pickle.dump(bb, f, pickle.HIGHEST_PROTOCOL)