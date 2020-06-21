import os
indicators_root_path = os.getcwd() + '/indicators/'

global_settings = { 
        'SNR' : {'period_size' : 64},
        'SMA' : {'period_size' : 200},
        'RSI' : {'period_size' : 14},
        'NLMS' : {  
                    'period_size' : 200,
                    'step_size' : 0.7,
                    'norm_constant' : 0.1
                 },
        'MFI' : {'period_size' : 14},
        'MACD' : {
                    'slow_period_size' : 26,
                    'fast_period_size' : 12,
                    'signal_period_size' : 9
                 },
        'IKH' : {
                    'wlen_conversion_line' : 9,
                    'wlen_base_line' : 26,
                    'wlen_leading_span2' : 52,
                    'wlen_displacement' : 26,
        },
        'EMA' : {'period_size' : 200},
        'CMF' : {'period_size' : 20},
        'CCI' : {'period_size' : 20},
        'BB' : {
                'period_size' : 40,
                'n_std' : 5
                },
        'ATR' : {'period_size' : 14},
        'ADX' : {'period_size' : 14},
      }
