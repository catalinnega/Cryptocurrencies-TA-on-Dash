import indicators.indicator_settings as indicator_settings

settings = indicator_settings.global_settings['NLMS']
table_name = "NLMS"
for i in list(settings.keys()):
    table_name += "_" + str(settings[i]).replace(".", "_")
settings.update(
    {
        'db_path' : indicator_settings.indicators_root_path + "/nlms/nlms_db.sqlite",
        'table_list' : (
                        ['timestamp', 'INT', 'NOT NULL'],
                        ['close', 'FLOAT(5,4)' , 'NOT NULL'],
                        ['error', 'FLOAT(5,4)' , 'NOT NULL'],
                        ['filter_output', 'FLOAT(5,4)' , 'NOT NULL'],
                        ['error_diff', 'FLOAT(5,4)' , 'NOT NULL'],
        ),
        'update_tdiff' : 4096,
        'table_name' : table_name
    }
)