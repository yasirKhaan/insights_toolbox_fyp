import pandas as pd
import pyodbc
import sys
import numpy as np

class CsvConnection():
    def __init__(self,csv_str,datasource_name,table_name):


        self.conn_str_sql = (
            r'DRIVER={SQL Server};'
            r'SERVER=(local);'
            r'DATABASE=milestone;'
            r'Trusted_Connection=yes;'
        )

        self.conn_sql = pyodbc.connect(self.conn_str_sql)
        self.cursor = self.conn_sql.cursor()

        self.conn_str_csv = csv_str

        # header = int(input("1 for yes, 0 for No"))
        header = 1
        if header == 1:
            self.conn_csv = pd.read_csv(self.conn_str_csv)
        else:
            self.conn_csv = pd.read_csv(self.conn_str_csv, header=None)

        # schema

        self.schema_name = datasource_name
        self.table_name = table_name

    def get_column(self):
        lst_of_col_and_type = [{
            'columns': []
        }, {
            'data_types': []
        }]

        for col in self.conn_csv.columns:
            lst_of_col_and_type[0]['columns'].append(col)
            if self.conn_csv[col].dtypes:
                if self.conn_csv[col].dtypes == 'int64':
                    lst_of_col_and_type[1]['data_types'].append('INT')
                elif self.conn_csv[col].dtypes == 'float64':
                    lst_of_col_and_type[1]['data_types'].append('FLOAT')
                elif self.conn_csv[col].dtypes == 'object':
                    lst_of_col_and_type[1]['data_types'].append('VARCHAR(50)')
                elif self.conn_csv[col].dtypes == 'bool':
                    lst_of_col_and_type[1]['data_types'].append('BIT')
        return (lst_of_col_and_type)
        # print (lst_of_col_and_type)

    def csv_to_sqltables(self):

        list_of_col = self.get_column()
        # print(list_of_col)

        schema_name = self.schema_name

        try:
            self.cursor.execute('CREATE SCHEMA ' + schema_name)
            self.cursor.commit()
        except:
            print("NAME OF DATABASE IS ALREADY EXIST CHANGE THE NAME")
            sys.exit()


        dts_index = 0
        try:
            query = 'CREATE TABLE ' + schema_name + '.'+self.table_name+' ('
            for cols in list_of_col[0]['columns']:
                query += cols + ' ' + list_of_col[1]['data_types'][dts_index] + ',\n'
                dts_index += 1
            query += ')'



            self.cursor.execute(query)
            self.cursor.commit()
        except:
            print("CHANGE THE TABLE NAME BECAUSE ALREADY EXIST")



    def csvdata_to_sql(self):


        conn_csv2 = self.conn_csv.replace(np.nan, '', regex=True)

        list_of_col = self.get_column()

        for record in conn_csv2.values:
            query = 'INSERT INTO ' + self.schema_name + '.'+self.table_name+' SELECT '
            for i in range(len(list_of_col[0]['columns'])):
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

            query += ' WHERE NOT EXISTS ( SELECT 1 FROM ' + self.schema_name + '.'+self.table_name+' WHERE '
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
            # print(query)
            self.cursor.execute(query)
            self.cursor.commit()

# var = 'C:\\Users\\KHURRAM\\Downloads\\sample dataset\\SAMPLECSV.csv'
# print(type(var))
# csv = CsvConnection(str(var),'CSV','csv_table')
# csv.get_column()
# csv.csv_to_sqltables()
# csv.csvdata_to_sql()  