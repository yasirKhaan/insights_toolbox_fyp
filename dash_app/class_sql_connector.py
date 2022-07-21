import pyodbc
from sqlalchemy import (create_engine, inspect, MetaData)

class SQLConnection():
    def __init__(self,driver, server, db_name, datasource_name):

        # self.server = server
        # self.driver = driver
        # self.database = 'first_db'
        # self.main_database = 'main_db'

        self.conn_str = (
            r'DRIVER={SQL Server};'
            r'SERVER=(local);'
            r'DATABASE=firstdb;'
            r'Trusted_Connection=yes;'
        )
        self.conn = pyodbc.connect(self.conn_str)
        self.cursor = self.conn.cursor()

        self.user_db = 'firstdb'
        self.user_schema = '.dbo.'
        self.main_db = 'milestone'
        self.main_schema = '.'+datasource_name+'.'
        self.datasource = datasource_name

        self.server = '(local)'
        self.driver = 'ODBC Driver 17 for SQL Server'
        self.database = 'firstdb'
        self.main_database = 'milestone'

        db_conn1 = f'mssql://@{self.server}/{self.database}?driver={self.driver}'
        db_conn2 = f'mssql://@{self.server}/{self.main_database}?driver={self.driver}'

        engine1 = create_engine(db_conn1)
        engine2 = create_engine(db_conn2)

        self.connection1 = engine1.connect()
        self.connection2 = engine2.connect()

    def create_tables_from_src_db(self):
        meta = MetaData()
        meta.reflect(self.connection1)
        meta.create_all(self.connection2)

    def identity_insert_off(self):
        tables_db = self.cursor.execute('SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES')
        tables_lst = []  # TO GET FORMATTED TABLE NAMES
        for raw_table_names in tables_db:  # WILL OPT RAW DATA LIKE (TABLENAME,)
            for formatted_table_names in raw_table_names:
                tables_lst.append(formatted_table_names)  # STORE FORMATTED NAMES OF TABLE
        for identity in range(len(tables_lst)):
            identity_query = 'SET IDENTITY_INSERT '+self.main_db + self.main_schema + tables_lst[identity]+' OFF;'
            self.cursor.execute(identity_query)

    def data_into_primary_db(self):
        tables_db = self.cursor.execute('SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES')
        tables_lst = []  # TO GET FORMATTED TABLE NAMES
        for raw_table_names in tables_db:  # WILL OPT RAW DATA LIKE (TABLENAME,)
            for formatted_table_names in raw_table_names:
                tables_lst.append(formatted_table_names)  # STORE FORMATTED NAMES OF TABLE
        sequenced_table = tables_lst

        raw_cols_query_user_db = ''
        lst_raw_cols_query_user_db = []
        left_over_tables = []
        left_over_queries = []
        for seq_table in range(len(sequenced_table)):
            for columns in self.cursor.columns(table=sequenced_table[seq_table]):
                raw_cols_query_user_db += '[' + columns.column_name + '], '
            formatted_cols = raw_cols_query_user_db[:-2:]
            lst_raw_cols_query_user_db.append(formatted_cols)
            raw_cols_query_user_db = ''
            self.identity_insert_off()
            insert_identity_query = 'SET IDENTITY_INSERT ' + self.main_db + self.main_schema + sequenced_table[seq_table] + ' ON;'
            insert_query_three = 'INSERT into ' + self.main_db + self.main_schema + sequenced_table[seq_table] + ' (' + \
                                 lst_raw_cols_query_user_db[seq_table] + ') SELECT ' + lst_raw_cols_query_user_db[
                                     seq_table] + ' FROM ' + self.user_db + self.user_schema + sequenced_table[seq_table] + ';'
            # print(insert_query_three)
            try:
                # print('try', sequenced_table[seq_table])
                self.cursor.execute(insert_identity_query)
                self.cursor.execute(insert_query_three)
                self.cursor.commit()
            except pyodbc.IntegrityError:
                # print('except 2 ',sequenced_table[seq_table])
                left_over_tables.append(sequenced_table[seq_table])
                left_over_queries.append(lst_raw_cols_query_user_db[seq_table])
            except pyodbc.ProgrammingError:
                pass

        # print("LEFT OVER",left_over_tables)
        # print("LEFT OVER QUERIES",left_over_queries)
        left_over_done = []
        rev = left_over_tables[::-1]
        rev_q = left_over_queries[::-1]
        for left_tables in range(len(rev)):
            try:
                if rev[left_tables] not in left_over_done:
                    self.identity_insert_off()
                    # print('creating',rev[left_tables] )
                    insert_identity_query = 'SET IDENTITY_INSERT ' + self.main_db + self.main_schema + rev[left_tables] + ' ON;'
                    insert_query_three = 'INSERT into ' + self.main_db + self.main_schema + rev[left_tables] + ' (' + rev_q[
                        left_tables] + ') SELECT ' + rev_q[left_tables] + ' FROM ' + self.user_db + self.user_schema + rev[
                                             left_tables] + ';'
                    self.cursor.execute(insert_identity_query)
                    # print(insert_identity_query)
                    # print(insert_query_three)
                    self.cursor.execute(insert_query_three)
                    self.cursor.commit()
                    left_over_done.append(rev[left_tables])
                    # print("To Check Added", left_over_done)
                    left_over_tables.remove(rev[left_tables])
                    # print("To Remove From Left Over", left_over_tables)
            except pyodbc.IntegrityError:
                reversed_tables_lst = left_over_tables[::-1]
                # print("REVERSE ",reversed_tables_lst)
                for rev_tables in range(len(reversed_tables_lst)):
                    if reversed_tables_lst[rev_tables] not in left_over_done:
                        # print('REVERSE TABLES IN EXCEPTION',rev_tables,reversed_tables_lst[rev_tables])
                        self.identity_insert_off()
                        insert_identity_query = 'SET IDENTITY_INSERT ' + self.main_db + self.main_schema + reversed_tables_lst[
                            rev_tables] + ' ON;'
                        insert_query_three = 'INSERT into ' + self.main_db + self.main_schema + reversed_tables_lst[
                            rev_tables] + ' (' + left_over_queries[rev_tables] + ') SELECT ' + left_over_queries[
                                                 rev_tables] + ' FROM ' + self.user_db + self.user_schema + reversed_tables_lst[
                                                 rev_tables] + ';'
                        # print('EXCEPT',insert_identity_query)
                        # print('EXCEPT',insert_query_three)
                        self.cursor.execute(insert_identity_query)
                        self.cursor.execute(insert_query_three)
                        self.cursor.commit()
                        left_over_done.append(reversed_tables_lst[rev_tables])
                        # print("EXCEPT To Check Added", left_over_done)
                        left_over_tables.remove(left_over_tables[left_tables])
                        # print("EXCEPT To Remove From Left Over", left_over_tables)
            # print('passing',left_over_tables[left_tables] )
        # print(lst_raw_cols_query_user_db)

    def transfer_schema(self):
        # schema_name = 'SQL'
        schema_name = self.datasource
        tables_db = self.cursor.execute('SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES')
        tables_lst = []  # TO GET FORMATTED TABLE NAMES
        for raw_table_names in tables_db:  # WILL OPT RAW DATA LIKE (TABLENAME,)
            for formatted_table_names in raw_table_names:
                tables_lst.append(formatted_table_names)  # STORE FORMATTED NAMES OF TABLE

        try:

            self.connection2.execute('CREATE SCHEMA ' + schema_name)

            for table_name in tables_lst:
                alteration = self.connection2.execute('ALTER SCHEMA ' + schema_name + ' TRANSFER dbo.' + table_name)
        except:
            print('CHANGE THE DATASOURCE NAEM ALREADY EXIST')
#
# sql = SQLConnection('a','b','c','SQL')
# (sql.create_tables_from_src_db())
# (sql.transfer_schema())
# (sql.data_into_primary_db())