import indicators.indicator_settings as indicator_settings

settings = indicator_settings.global_settings['SNR']
table_name = "SNR"
for i in list(settings.keys()):
    table_name += "_" + str(settings[i])
settings.update(
    {
        'db_path' : indicator_settings.indicators_root_path + "/snr/snr_db.sqlite",
        'table_list' : (
                        ['timestamp', 'INT', 'NOT NULL'],
                        ['close', 'FLOAT(5,4)' , 'NOT NULL'],
                        ['snr', 'FLOAT(5,4)' , 'NOT NULL'],
        ),
        'update_tdiff' : 4096,
        'table_name' : table_name
    }
)