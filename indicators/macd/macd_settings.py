import indicators.indicator_settings as indicator_settings

settings = indicator_settings.global_settings['MACD']
table_name = "MACD"
for i in list(settings.keys()):
    table_name += "_" + str(settings[i])
settings.update(
    {
        'db_path' : indicator_settings.indicators_root_path + "/macd/macd_db.sqlite",
        'table_list' : (
                        ['timestamp', 'INT', 'NOT NULL'],
                        ['close', 'FLOAT(5,4)' , 'NOT NULL'],
                        ['fast_ema', 'FLOAT(5,4)' , 'NOT NULL'],
                        ['slow_ema', 'FLOAT(5,4)' , 'NOT NULL'],
                        ['signal_line', 'FLOAT(5,4)' , 'NOT NULL'],
                        ['macd', 'FLOAT(5,4)' , 'NOT NULL'],
                        ['macd_histogram', 'FLOAT(5,4)' , 'NOT NULL'],
        ),
        'update_tdiff' : 4096,
        'table_name' : table_name
    }
)