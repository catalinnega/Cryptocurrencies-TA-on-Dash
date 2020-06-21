import indicators.indicator_settings as indicator_settings

settings = indicator_settings.global_settings['BB']
table_name = "BB"
for i in list(settings.keys()):
    table_name += "_" + str(settings[i])
settings.update(
    {
        'db_path' : indicator_settings.indicators_root_path + "/bb/bb_db.sqlite",
        'table_list' : (
                    ['timestamp', 'INT', 'NOT NULL'],
                    ['input', 'FLOAT(5,4)' , 'NOT NULL'],
                    ['sma', 'FLOAT(5,4)' , 'NOT NULL'],
                    ['upperline', 'FLOAT(5,4)' , 'NOT NULL'],
                    ['lowerline', 'FLOAT(5,4)' , 'NOT NULL'],
                    ['squeeze', 'FLOAT(5,4)' , 'NOT NULL'],
        ),
        'update_tdiff' : 4096,
        'table_name' : table_name
    }
)