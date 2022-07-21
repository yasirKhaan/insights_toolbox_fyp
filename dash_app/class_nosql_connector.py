from pymongo import MongoClient
import pyodbc
import sys


class NoSQLConnection():
    def __init__(self,nosql_str,db_name,table_name,datasource_name):

        # self.conn_str_nsql = "mongodb://localhost:27017/first_db_nsql"
        self.conn_str_nsql = str(nosql_str)


        self.conn_str_sql = (
            r'DRIVER={SQL Server};'
            r'SERVER=(local);'
            r'DATABASE=milestone;'
            r'Trusted_Connection=yes;'
        )

        self.main_db = 'milestone'
        self.main_schema = '.dbo.'


        self.conn = pyodbc.connect(self.conn_str_sql)
        self.cursor = self.conn.cursor()

        self.client = MongoClient(self.conn_str_nsql)
        # self.db = self.client['first_db_nsql']
        # self.db_name = str(db_name)
        self.db = self.client[db_name]
        # self.collection = self.db['nsql_table']
        self.table_name = str(table_name)
        self.collection = self.db[self.table_name]

        self.schema_name = datasource_name
        # self.table_name = table_name

    def get_keys_in_lst(self):
        lst_of_keys = [{
            'columns': []
        }, {
            'data_types': []
        }]
        for records in self.collection.find({}, {"_id": 0}):
            for keys, values in records.items():
                if keys not in lst_of_keys[0]['columns']:
                    lst_of_keys[0]['columns'].append(keys)
                    if type(values):
                        if type(values) == int:
                            lst_of_keys[1]['data_types'].append('INT')
                        elif type(values) == str:
                            lst_of_keys[1]['data_types'].append('VARCHAR(50)')
                        elif type(values) == bool:
                            lst_of_keys[1]['data_types'].append('BIT')
        # print(type(lst_of_keys[0]))
        # print(lst_of_keys)
        return lst_of_keys

    def nsql_to_sql_tables(self):

        schema_name = self.schema_name  # will be user-defined later

        list_of_keys = self.get_keys_in_lst()
        # print(list_of_keys)

        try:
            self.cursor.execute('CREATE SCHEMA ' + schema_name)
            self.cursor.commit()
        except:
            print("NAME OF DATABASE IS ALREADY EXIST CHANGE THE NAME")
            sys.exit()


        dts_index = 0
        try:

            query = 'CREATE TABLE ' + schema_name + '.'+self.table_name+' ('
            for cols in list_of_keys[0]['columns']:
                query += cols + ' ' + list_of_keys[1]['data_types'][dts_index] + ',\n'
                print(list_of_keys[1]['data_types'][dts_index])
                dts_index += 1

            query += ')'

            print(query)


            self.cursor.execute(query)
            self.cursor.commit()
        except:
            print("CHANGE THE TABLE NAME BECAUSE ALREADY EXIST")
        #
        # self.cursor.execute('CREATE SCHEMA ' + schema_name)
        # self.cursor.commit()
        # self.cursor.execute('ALTER SCHEMA ' + schema_name + ' TRANSFER dbo.' + 'nsql_table')
        # self.cursor.commit()

    def nsql_data_to_sql(self):
        main_schema = self.schema_name

        r_lst_of_values = []
        for dictionary in self.collection.find({}, {"_id": 0}):
            itr_lst = []
            for values in dictionary.values():
                itr_lst.append(values)

            r_lst_of_values.append(tuple(itr_lst))

        list_of_col = self.get_keys_in_lst()


        for record in r_lst_of_values:
            query = 'INSERT INTO ' + main_schema + '.'+self.table_name+' SELECT '
            for i in range(len(list_of_col[0]['columns'])):

                record = list(record)

                if record[i] == True:
                    record[i] = 1

                elif record[i] == False:
                    record[i] = 0

                if i != len(list_of_col[0]['columns']) - 1:
                    if list_of_col[1]['data_types'][i] == 'VARCHAR(50)':
                        query += "'" + str(record[i]) + "'" + ','
                    else:
                        query += str(record[i]) + ','
                else:
                    if list_of_col[1]['data_types'][i] == 'VARCHAR(50)':
                        query += "'" + str(record[i]) + "'"
                    else:
                        query += str(record[i])

            query += ' WHERE NOT EXISTS ( SELECT 1 FROM ' + main_schema + '.'+self.table_name+' WHERE '
            for j in range(len(list_of_col[0]['columns'])):
                if j != len(list_of_col[0]['columns']) - 1:
                    if list_of_col[1]['data_types'][j] == 'VARCHAR(50)':
                        query += list_of_col[0]['columns'][j] + ' = ' + "'" + str(record[j]) + "'" + ' AND '
                    else:
                        query += list_of_col[0]['columns'][j] + ' = ' + str(record[j]) + ' AND '
                else:
                    if list_of_col[1]['data_types'][j] == 'VARCHAR(50)':
                        query += list_of_col[0]['columns'][j] + ' = ' + "'" + str(record[j]) + "'" + ')'
                    else:
                        query += list_of_col[0]['columns'][j] + ' = ' + str(record[j]) + ')'

            self.cursor.execute(query)
            self.cursor.commit()




# nosql = NoSQLConnection('mongodb://localhost:27017/first_db_nsql','first_db_nsql','nsql_table','NOSQL')
# print(nosql.get_keys_in_lst())
# (nosql.nsql_to_sql_tables())
# (nosql.nsql_data_into_sql())