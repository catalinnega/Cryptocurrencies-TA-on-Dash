import sqlite3
import pandas as pd
import dash_app.dash_settings as ds
import plotly.graph_objs as go
from indicators.indicator_libs import indicators_list

def get_labels():
    labels = []
    for i in range(len(indicators_list)):
        labels.append({'label': indicators_list[i]['name'], 'value': indicators_list[i]['id']})
    return labels

def get_vals(indicator_id):
    for indicator_dict in indicators_list:
        if(indicator_dict['id'] == indicator_id):
            db_path = indicator_dict['settings']['db_path']
            table_name = indicator_dict['settings']['table_name']
    con = sqlite3.connect(db_path)
    df = pd.read_sql_query(f"select * from {table_name} ORDER BY timestamp DESC LIMIT {ds.QUEUE_LEN}", con)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df.to_dict('list')