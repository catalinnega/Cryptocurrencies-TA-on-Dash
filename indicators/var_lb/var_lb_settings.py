import indicators.indicator_settings as indicator_settings

settings = indicator_settings.global_settings['VAR_LB']
table_name = "VAR_LB"
for i in list(settings.keys()):
    table_name += "_" + str(settings[i])
settings.update(
    {
        'db_path' : indicator_settings.indicators_root_path + "/var_lb/var_lb_db.sqlite",
        'table_list' : (
                        ['timestamp', 'INT', 'NOT NULL'],
                        ['close', 'FLOAT(5,4)' , 'NOT NULL'],
                        ['apriori_var', 'FLOAT(5,4)' , 'NOT NULL'],
                        ['aposteriori_mean', 'FLOAT(5,4)' , 'NOT NULL'],
                        ['labels', 'INT' , 'NOT NULL'],
        ),
        'update_tdiff' : 4096,
        'table_name' : table_name
    }
)