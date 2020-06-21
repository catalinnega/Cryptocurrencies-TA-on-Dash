import indicators.indicator_settings as indicator_settings

settings = indicator_settings.global_settings['CCI']
table_name = "CCI"
for i in list(settings.keys()):
    table_name += "_" + str(settings[i])
settings.update(
    {
        'db_path' : indicator_settings.indicators_root_path + "/cci/cci_db.sqlite",
        'table_list' : (
                    ['timestamp', 'INT', 'NOT NULL'],
                    ['close', 'FLOAT(5,4)' , 'NOT NULL'],
                    ['high', 'FLOAT(5,4)' , 'NOT NULL'],
                    ['low', 'FLOAT(5,4)' , 'NOT NULL'],
                    ['volume', 'FLOAT(5,4)' , 'NOT NULL'],
                    ['cci', 'FLOAT(5,4)' , 'NOT NULL'],
        ),
        'update_tdiff' : 4096,
        'table_name' : table_name
    }
)