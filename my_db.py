import sqlite3
import pandas as pd

class DB:
    def __init__(self, **kwargs):
        self.path = kwargs['db_path']
        self.table_name = kwargs['table_name']
        self.table_list = kwargs['table_list']
        self.db = sqlite3.connect(self.path)
        self.tables_dict = {}
        self.create_DB()
    
    def create_DB(self):
        cmd_fields = ' '.join([' '.join(i) + ',' for i in self.table_list])
        cmd_fields = cmd_fields[:-1]
        cmd = f"create table if not exists {self.table_name}({cmd_fields});"
        self.db.execute(cmd)

    def close(self):
        self.db.close()
        
    def create_table(self, vals_list, table_name):
        cmd_fields = ' '.join([' '.join(i) + ',' for i in vals_list])
        cmd = f"CREATE TABLE IF NOT EXISTS \
                {table_name}({cmd_fields} \
                PRIMARY KEY ({vals_list[0][0]}));"
        self.update_tables_dict(vals_list, table_name)
        print('\n', cmd)
        self.db.execute(cmd)
    
        
    def insert_features(self, table_name, samples, replace_last_value = False):
        def generator():
            for i in samples:
                yield i
        
        if(replace_last_value):
            self.replace_last(samples[0])
        
        cols = self.tables_dict[table_name]['col_names']
        cols_cmd = ''
        for i in cols: cols_cmd += i + ', '
        cols_cmd = cols_cmd[:-2]
        
        sql_placeholders = ' '.join(["?," for _ in range(len(cols))])
        sql_placeholders = sql_placeholders[:-1]
        
        with self.db:
            cmd = "INSERT INTO %s \
                    (%s) \
                    VALUES (%s)" \
                    % (table_name,
                       cols_cmd,
                       sql_placeholders)
            
            #print('\n', cmd)
            self.db.executemany(cmd, generator())
            
    def left_join(self, new_table, left_table, right_tables, common_cols, join_col):
        left_cols = self.tables_dict[left_table]['col_names']
        left_cols = [left_table + '.' + i + ' AS ' + i +','  for i in left_cols]
        left_cols_cmd = ' '.join(left_cols)
        
        right_cols_cmd = ''
        left_join_cmd = ''
        for right_table in right_tables:
            right_cols = self.tables_dict[right_table]['col_names']
            [right_cols.remove(i) for i in common_cols]
            right_cols_cmd += ' '
            tmp_cmd = [right_table + '.' + i + ' AS ' + i +',' for i in right_cols]
            right_cols_cmd += ' '.join(tmp_cmd)
            left_join_cmd += ' LEFT JOIN ' + right_table
        right_cols_cmd = right_cols_cmd[:-1] ## remove last character (which is ',')
        
        
        cmd = "CREATE TABLE IF NOT EXISTS %s \
                AS SELECT %s \
                %s \
                FROM %s \
                %s \
                using(%s) \
                GROUP BY %s;"\
                % (new_table,
                   left_cols_cmd,
                   right_cols_cmd,
                   left_table,
                   left_join_cmd,
                   join_col,
                   left_table + ".time")
        print('\n', cmd)
        self.db.execute(cmd) 
        

        vals_list = []
        tables = [left_table]
        tables.extend(right_tables)
        for name in tables:
            cols = self.tables_dict[name]['col_names']
            types = self.tables_dict[name]['types']
            options = self.tables_dict[name]['options']
            vals_list.extend([cols[i], types[i], options[i]] for i in range(len(cols)))
        self.update_tables_dict(vals_list, new_table)
        
    def get_latest_time(self, symbol, table_name, time_key):
        cmd = ''
        if(symbol):
          cmd = f"where symbol={symbol}"
        r = self.db.execute(f"select max({time_key}) from {table_name} {cmd}")
        result = r.fetchone()[0]
        return result
    
    def select_latest_interval(self, table_name, symbol, interval):
        r = self.db.execute('select * from %s where symbol=%s order by time desc limit %d' % (table_name, symbol, interval))
        result = r.fetchall()
        return result
    
    def select_interval(self, table_name, symbol, interval):
        r = self.db.execute(f"select * from {table_name} where time between {interval[0]} and {interval[1]} order by time")
        result = r.fetchall()
        return result
    
    def update_tables_dict(self, vals_list, table_name):
        col_names = [i[0] for i in vals_list]
        types = [i[1] for i in vals_list]
        options = [i[2] for i in vals_list]
        self.tables_dict.update({table_name: {'col_names' : col_names, 'types': types, 'options': options}})
    
    def replace_last(self, vals):
        cmd_latest = f"select * from {self.table_name} ORDER BY timestamp DESC LIMIT 1"
        print(cmd_latest)
        try:
            df = pd.read_sql_query(cmd_latest, self.db)
        except:
            print("Could not replace latest value")
            return
        if(len(df.values) != 0):
            cols = ','.join(list(df.columns.values))
            vals = ",".join(map(str, vals))
            cmd = f"REPLACE INTO {self.table_name} ({cols}) VALUES ({vals})"
            print(cmd)
            self.db.execute(cmd)
        else:
            print("Could not replace latest value")

class UpdateDB(DB):
    def __init__(self, obj, **kwargs):
        self.table_name = kwargs['table_name']
        self.table_list = kwargs['table_list']
        self._update_tdiff = kwargs['update_tdiff']
        self._replace_last_value = kwargs['replace_last']
        self.reset_method = obj.reset_bufs
        self.__is_db = False
        self.is_flush = False
        super().__init__(**kwargs)

    def update_db(self, vals, use_accum = True):
        if(use_accum):
            if(len(vals) < self._update_tdiff) and not self.flush:
                return
        if not self.__is_db:
            self.create_table(self.table_list, self.table_name)
            self.__is_db = True
        self.insert_features(self.table_name, vals, self._replace_last_value)
        self.reset_method()
        self.is_flush = False

    def flush_db(self, vals):
        self.is_flush = True
        self.update_db(vals)
        self.reset_method()

    def fetch_latest_data(self, wlen):
        df = None
        try:
            df = pd.read_sql_query(f"select * from {self.table_name} ORDER BY timestamp DESC LIMIT {wlen}", self.db)
        except AttributeError as e:
            print('Database empty.', e)
        return df
