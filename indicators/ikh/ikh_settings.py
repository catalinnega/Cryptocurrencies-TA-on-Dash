import indicators.indicator_settings as indicator_settings

settings = indicator_settings.global_settings['IKH']
table_name = "IKH"
for i in list(settings.keys()):
    table_name += "_" + str(settings[i])
settings.update(
    {
        'db_path' : indicator_settings.indicators_root_path + "/ikh/ikh_db.sqlite",
        'table_list' : (
                        ['timestamp', 'INT', 'NOT NULL'],
                        ['close', 'FLOAT(5,4)' , 'NOT NULL'],
                        ['conversion_line', 'FLOAT(5,4)' , 'NOT NULL'],
                        ['base_line', 'FLOAT(5,4)' ,'NOT NULL'],
                        ['leading_span_A', 'FLOAT(5,4)' ,'NOT NULL'],
                        ['leading_span_B', 'FLOAT(5,4)' ,'NOT NULL']
        ),
        'update_tdiff' : 4096,
        'table_name' : table_name
    }
)