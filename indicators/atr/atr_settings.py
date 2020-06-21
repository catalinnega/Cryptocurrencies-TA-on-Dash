import indicators.indicator_settings as indicator_settings

settings = indicator_settings.global_settings['ATR']
table_name = "ATR"
for i in list(settings.keys()):
    table_name += "_" + str(settings[i])
settings.update(
    {
        'db_path' :  indicator_settings.indicators_root_path + "/atr/atr_db.sqlite",
        'table_list' : (
                    ['timestamp', 'INT', 'NOT NULL'],
                    ['close', 'FLOAT(5,4)' , 'NOT NULL'],
                    ['true_range', 'FLOAT(5,4)' , 'NOT NULL'],
                    ['atr', 'FLOAT(5,4)' , 'NOT NULL'],
        ),
        'update_tdiff' : 4096,
        'table_name' : table_name
    }
)