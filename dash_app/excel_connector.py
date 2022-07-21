import pandas as pd
import pyodbc
import sys
import numpy as np

class ExcelConnection():
    def __init__(self,excel_str,datasource_name,table_name):
# SQL CONNECTION

        self.conn_str_sql = (
            r'DRIVER={SQL Server};'
            r'SERVER=DESKTOP-2F5VLJ7;'
            r'DATABASE=milestone;'
            r'Trusted_Connection=yes;'
        )

        self.conn_sql = pyodbc.connect(self.conn_str_sql)
        self.cursor = self.conn_sql.cursor()

# EXCEL CONNECTION
        self.conn_str_excel = excel_str

# default_sheet = int(input("1 for yes, 0 for no"))
        default_sheet = 1
# header = int(input("1 for yes, 0 for no"))
        header = 1

        if default_sheet == 1:
            if header == 1:
                # conn_str_excel = r"C:\Users\KHURRAM\Downloads\testing.xlsx"
                self.conn_excel = pd.read_excel(self.conn_str_excel)
                # print(conn_excel)
            else:
                self.conn_excel = pd.read_excel(self.conn_str_excel, header=None)
                # conn_str_excel = r"C:\Users\KHURRAM\Downloads\testing.xlsx"

            # print(conn_excel)

        else:
            if header == 1:

                ask = str(input("sheet name ?"))
                # conn_str_excel = r"C:\Users\KHURRAM\Downloads\testing.xlsx"
                self.conn_excel = pd.read_excel(self.conn_str_excel, sheet_name=ask)
                # print(conn_excel)
            else:
                ask = str(input("sheet name ?"))
                # self.conn_str_excel = r"C:\Users\KHURRAM\Downloads\testing.xlsx"
                self.conn_excel = pd.read_excel(self.conn_str_excel, sheet_name=ask, header=None)
                # print(conn_excel)

        self.schema_name = datasource_name
        self.table_name = table_name



    def get_column(self):

        lst_of_col_and_type = [{
            'columns': []
        }, {
            'data_types': []
        }]

        for col in self.conn_excel.columns:
            lst_of_col_and_type[0]['columns'].append(col)
            if self.conn_excel[col].dtypes:
                if self.conn_excel[col].dtypes == 'int64':
                    lst_of_col_and_type[1]['data_types'].append('INT')
                elif self.conn_excel[col].dtypes == 'float64':
                    lst_of_col_and_type[1]['data_types'].append('FLOAT')
                elif self.conn_excel[col].dtypes == 'object':
                    lst_of_col_and_type[1]['data_types'].append('VARCHAR(50)')
                elif self.conn_excel[col].dtypes == 'bool':
                    lst_of_col_and_type[1]['data_types'].append('BIT')

    # print(lst_of_col_and_type)
        return(lst_of_col_and_type)

# get_column(conn_excel)

    def excel_to_sqltables(self):

        list_of_col = self.get_column()
        # print(list_of_col)

        schema_name = self.schema_name

        try:
            self.cursor.execute('CREATE SCHEMA ' + schema_name)
            self.cursor.commit()
        except:
            print("CHANGE")
            # print(schema_name)
            sys.exit()


        dts_index = 0
        try:
            query = 'CREATE TABLE ' + schema_name + '.' + self.table_name + ' ('
            for cols in list_of_col[0]['columns']:
                query += cols + ' ' + list_of_col[1]['data_types'][dts_index] + ',\n'
                dts_index += 1
            query += ')'

            self.cursor.execute(query)
            self.cursor.commit()

        except:
            print("CHANGE THE TABLE NAME BECAUSE ALREADY EXIST")


# excel_to_sqltables(schema_name)

    def exceldata_to_sql(self):


        conn_csv2 = self.conn_excel.replace(np.nan, '', regex=True)

        list_of_col = self.get_column()
    # print(len(list_of_col[0]['columns']))

    # for i in range(6):
        for record in conn_csv2.values:
            query = 'INSERT INTO ' + self.schema_name + '.' + self.table_name + ' SELECT '
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

            query += ' WHERE NOT EXISTS ( SELECT 1 FROM ' + self.schema_name + '.' + self.table_name + ' WHERE '
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




