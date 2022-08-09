from sqlite3 import ProgrammingError
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
import pyodbc 
import json
import pandas as pd 
import csv
import pyexcel
import openpyxl

conn_str = (
    r'DRIVER=ODBC Driver 17 for SQL Server;'
    r'SERVER=DESKTOP-BVT6U1A\MSSQLSERVER01;'
    r'DATABASE=cust_db;'
    r'Trusted_Connection=yes;'
)

conn = pyodbc.connect(conn_str)
cursor = conn.cursor()



def data_update(request):
    print("data_update")
    old_schema = request.POST.get("old_schema")
    new_schema = request.POST.get("new_schema")

    existing_schema = request.POST.get("existing_schema")
    present_schema = request.POST.get("present_schema")
    # print(existing_schema)
    # print(present_schema)

    if old_schema != "None" and new_schema != "None": 
        print("old_schema ", old_schema)
        print("new_schema ", new_schema)
        print("Transfer To New Schema")
    #     print(old_schema)
        # tables_db = cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '{}';".format(str(old_schema)))
        # tables_lst = []  # TO GET FORMATTED TABLE NAMES
        # for raw_table_names in tables_db:  # WILL OPT RAW DATA LIKE (TABLENAME,)
        #     for formatted_table_names in raw_table_names:
        #         tables_lst.append(formatted_table_names)  # STORE FORMATTED NAMES OF TABLE
        # print("TABLES LIST ", tables_lst)


        # try:
        #     cursor.execute('DROP SCHEMA IF EXISTS ' + new_schema + ';')
        #     cursor.execute('CREATE SCHEMA ' + new_schema)
        #     for table_name in tables_lst:
        #         cursor.execute('ALTER SCHEMA {} TRANSFER {}.{}'.format(new_schema, old_schema, table_name))
        #         cursor.commit()
        # except ProgrammingError:
        #     print("EXCEPTION HIT \n")
        #     return HttpResponse("<h1>Error Detected</h1>")

    if existing_schema != "None" and present_schema != "None":
        print("Schema Transfer To Existing Schema")
        print(existing_schema)
        print(present_schema)


    return render(request, 'app_file/data_update.html')













def transfer_schema(schema_name):
    # schema_name = 'SQL'
    # schema_name = self.datasource
    print("IN transfer_schema")
    tables_db = cursor.execute('SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES')
    tables_lst = []  # TO GET FORMATTED TABLE NAMES
    for raw_table_names in tables_db:  # WILL OPT RAW DATA LIKE (TABLENAME,)
        for formatted_table_names in raw_table_names:
            tables_lst.append(formatted_table_names)  # STORE FORMATTED NAMES OF TABLE
    print("TABLES LIST ", tables_lst)
    
    print("TRY SECTION  ")
    cursor.execute('DROP SCHEMA IF EXISTS ' + schema_name + ';')
    cursor.execute('CREATE SCHEMA ' + schema_name)

    for table_name in tables_lst:
        cursor.execute('ALTER SCHEMA ' + schema_name + ' TRANSFER dbo.' + table_name)
        cursor.commit()
    # except:
    #     print('CHANGE THE DATASOURCE, NAME ALREADY EXIST')



def drop_mongo_table(table_name):
    cursor.execute("DROP TABLE IF EXISTS " + table_name + ";")
    cursor.commit()

def query_insertion(json_values, table_name):
    iterator_insert_query = "INSERT into " + table_name  + " VALUES ("
    for i in range(len(json_values)):
        temp = str(json_values[i])
        iterator_insert_query+= "'"+temp+"',"
    if iterator_insert_query[len(iterator_insert_query)-1] == ",":
        iterator_insert_query = iterator_insert_query[:len(iterator_insert_query)-1]
    iterator_insert_query+=");"
    return iterator_insert_query 

def query_creation(json_keys, json_values, table_name):
    list_of_data_types = []
    
    for data_type in json_values:
        if type(data_type) == int:
            list_of_data_types.append('INT')
        elif type(data_type) == str:
            list_of_data_types.append('VARCHAR(1000)')
        elif type(data_type) == bool:
            list_of_data_types.append('BIT')
    
    drop_mongo_table(table_name)
    create_query = "CREATE TABLE " + table_name + " ("
    
    for each_value in range(len(json_keys)):
        create_query+= " "+ json_keys[each_value] + " " + list_of_data_types[each_value] + ", \n"
    create_query+="); \n \n"
    return create_query
    





def mongo_data(request):
    if request.method == "POST":
        var2 = request.FILES['myfile']
        table_name = request.POST.get('table_title')
        table_schema_value = request.POST.get('table_schema_user_defined')

        # print("table_name ", table_name)
        # print("CREATING TABLE")
        if var2:
            json_format_data=json.load(var2)
            json_keys = list(json_format_data[0].keys())
            json_values = list(json_format_data[0].values())
            # print("json_values ", json_values)
            # print()

            json_valuesII = json_format_data
            # for i in range(len(json_valuesII)):
            #     print("json_values ", list(json_valuesII[i].values()))

            # iterator_insert_query = "INSERT into " + table_name  + " VALUES ("
            # for each_dict in range(len(json_valuesII)):
            #     # print(json_valuesII[each_dict])
            #     # print()
            #     # print(json_valuesII[each_dict].keys())
            #     for each_value in json_valuesII[each_dict].keys():
            #         print(each_value)
            #         # print(each_dict[each_value])
            #         temp = str(each_value)
            #         iterator_insert_query+= "'"+temp+"',"
            #     if iterator_insert_query[len(iterator_insert_query)-1] == ",":
            #         iterator_insert_query = iterator_insert_query[:len(iterator_insert_query)-1]
            #     iterator_insert_query+=");"

            # print(iterator_insert_query )
            iterator_insert_query = "INSERT into " + table_name  + " VALUES "
            # print(json_valuesII)
            count_checker = 0
            # print(len(json_valuesII))
            # while count_checker != len(json_valuesII)-1:
            for i in range(len(json_valuesII)):
                # print(json_valuesII[i])
                iterator_insert_query+= "("
                for each_value in json_valuesII[i].values():
                    # print(each_value)
                    temp = str(each_value).replace("'","")
                    iterator_insert_query+= "'"+temp+"',"
                    # count_checker+=1
                if iterator_insert_query[len(iterator_insert_query)-1] == ",":
                    iterator_insert_query = iterator_insert_query[:len(iterator_insert_query)-1]
                    if count_checker == len(json_valuesII)-1: 
                        iterator_insert_query+=")"
                    else:
                        iterator_insert_query+="), "
                # print("\n COUNT --> \n", count_checker)
                if count_checker == len(json_valuesII)-1:
                    # print("** -- count Checker Triggered -- **")
                    iterator_insert_query+=";"
                else:
                    count_checker+=1
            # for i in range(len(json_values)):
            #     temp = str(json_values[i])
            #     iterator_insert_query+= "'"+temp+"',"
            # if iterator_insert_query[len(iterator_insert_query)-1] == ",":
            #     iterator_insert_query = iterator_insert_query[:len(iterator_insert_query)-1]
            # iterator_insert_query+=");"
            print(iterator_insert_query )


            # return iterator_insert_query 
            cursor.execute(query_creation(json_keys, json_values, table_name))
            cursor.commit()
            # cursor.execute(query_insertion(json_values, table_name))
            cursor.execute(iterator_insert_query)
            cursor.commit()
        if table_schema_value:
            tables_db = cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'dbo'")
            tables_lst = []  # TO GET FORMATTED TABLE NAMES
            for raw_table_names in tables_db:  # WILL OPT RAW DATA LIKE (TABLENAME,)
                for formatted_table_names in raw_table_names:
                    tables_lst.append(formatted_table_names)  # STORE FORMATTED NAMES OF TABLE
            print(tables_lst)

            cursor.execute('DROP SCHEMA IF EXISTS ' + table_schema_value + ';')
            cursor.execute('CREATE SCHEMA ' + table_schema_value)

            try:
                for table_name in tables_lst:
                    cursor.execute('ALTER SCHEMA ' + table_schema_value + ' TRANSFER dbo.' + table_name)
                    cursor.commit()
            except ProgrammingError:
                pass
            print("Values Inserted")














        # print(query_creation(json_keys, json_values, "nsql_table"))
        # nosql_table = "nsql_table"
        # for data_type in json_values:
        #     if type(data_type) == int:
        #         list_of_data_types.append('INT')
        #     elif type(data_type) == str:
        #         list_of_data_types.append('VARCHAR(50)')
        #     elif type(data_type) == bool:
        #         list_of_data_types.append('BIT')
        # create_query = "CREATE TABLE " + nosql_table + " ("
        # for each_value in range(len(json_keys)):
        #     create_query+= " "+ json_keys[each_value] + " " + list_of_data_types[each_value] + ", \n"
        # create_query+="); \n \n"



        # iterator_insert_query = "INSERT into " + "nsql_table " + "VALUES ("
        # for i in range(len(json_values)):
        #     temp = str(json_values[i])
        #     iterator_insert_query+= "'"+temp+"',"
        # if iterator_insert_query[len(iterator_insert_query)-1] == ",":
        #     iterator_insert_query = iterator_insert_query[:len(iterator_insert_query)-1]
        # iterator_insert_query+=");"
        # print(iterator_insert_query)



    return render(request, "app_file/index.html")




def sql_data(request):
    table_create_query = request.POST.get('table_create')
    values_insert_query = request.POST.get('values_insert')
    table_schema_value = request.POST.get('table_schema_user_defined')
    print(table_create_query)
    # print(values_insert_query)    
    print(table_schema_value)


    
    if table_create_query:
        table_create_query = table_create_query.replace("go", "")
        cursor.execute(table_create_query)
        cursor.commit()

    if values_insert_query:
        cursor.execute(values_insert_query)
        cursor.commit()
    
    if table_schema_value:
        print(table_schema_value)
        # cursor.execute(transfer_schema(str(table_schema_value)))
        # tables_db = cursor.execute('SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES')
        tables_db = cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'dbo'")
        tables_lst = []  # TO GET FORMATTED TABLE NAMES
        for raw_table_names in tables_db:  # WILL OPT RAW DATA LIKE (TABLENAME,)
            for formatted_table_names in raw_table_names:
                tables_lst.append(formatted_table_names)  # STORE FORMATTED NAMES OF TABLE
        print(tables_lst)
        
# ("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'dbo'")


        # print("TABLES LIST ", tables_lst)
        
        # print("TRY SECTION  ")

        cursor.execute('DROP SCHEMA IF EXISTS ' + table_schema_value + ';')
        cursor.execute('CREATE SCHEMA ' + table_schema_value)

        try:
            for table_name in tables_lst:
                if table_name == "Order":
                    cursor.execute('ALTER SCHEMA ' + table_schema_value + ' TRANSFER dbo.' + '"' + table_name + '"')
                    cursor.commit()
                else:
                    cursor.execute('ALTER SCHEMA ' + table_schema_value + ' TRANSFER dbo.' + table_name)
                    cursor.commit()
        except ProgrammingError:
            pass




    # if schema_checker_value:
    #     pass

    return render(request, 'app_file/sql.html')


def csv_data(request):
    if request.method == "POST":
        var2 = request.FILES['csv_file'].read().splitlines()
        table_name = request.POST.get('table_title')
        table_schema_value = request.POST.get('table_schema_user_defined')

        parent_list_values = []
        # headers = request.POST['contain_header']
        if var2:
            for i in var2:
                temp = str(i).replace("'","")
                temp_lst= temp.split(",")
                splitted_lst = []
                for splitted in range(1,len(temp_lst)):
                    splitted_lst.append(temp_lst[splitted])
                parent_list_values.append(splitted_lst)

            iterator_insert_query = "INSERT into " + table_name  + " VALUES "
            count_checker = 0
            for each_list in range(len(parent_list_values)):
                iterator_insert_query+= "("
                for each_value in parent_list_values[each_list]:
                    iterator_insert_query+= "'"+each_value+"',"

                if iterator_insert_query[len(iterator_insert_query)-1] == ",":
                    iterator_insert_query = iterator_insert_query[:len(iterator_insert_query)-1]
                    if count_checker == len(parent_list_values)-1: 
                        iterator_insert_query+=")"
                    else:
                        iterator_insert_query+="), "
                # print("\n COUNT --> \n", count_checker)
                if count_checker == len(parent_list_values)-1:
                    # print("** -- count Checker Triggered -- **")
                    iterator_insert_query+=";"
                else:
                    count_checker+=1

            output = query_creation(parent_list_values[0], parent_list_values[1], table_name)
            cursor.execute(output)
            cursor.commit()
            cursor.execute(iterator_insert_query)
            cursor.commit()
        if table_schema_value:
            tables_db = cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'dbo'")
            tables_lst = []  # TO GET FORMATTED TABLE NAMES
            for raw_table_names in tables_db:  # WILL OPT RAW DATA LIKE (TABLENAME,)
                for formatted_table_names in raw_table_names:
                    tables_lst.append(formatted_table_names)  # STORE FORMATTED NAMES OF TABLE
            print(tables_lst)
            

            try:
                cursor.execute('DROP SCHEMA IF EXISTS ' + table_schema_value + ';')
                cursor.execute('CREATE SCHEMA ' + table_schema_value)
                for table_name in tables_lst:
                    cursor.execute('ALTER SCHEMA ' + table_schema_value + ' TRANSFER dbo.' + table_name)
                    cursor.commit()
            except ProgrammingError:
                pass
            print("Values Inserted")


    # for i in parent_list_values:
    #     print("parent_list_values --> ", i)
    # print()
    # print()
    # print()
    # print(iterator_insert_query)

            # print(temp_lst)

    return render(request, 'app_file/csv.html')


def excel_query_creation(data_headers, data_list, table_name):
    list_of_data_types = []
    
    for data_type in data_list[0]:
        if type(data_type) == int:
            list_of_data_types.append('INT')
        elif type(data_type) == str:
            list_of_data_types.append('VARCHAR(1000)')
        elif type(data_type) == bool:
            list_of_data_types.append('BIT')
    
    # drop_mongo_table(table_name)
    create_query = "CREATE TABLE " + table_name + " ("
    
    for each_value in range(len(data_headers)):
        create_query+= " "+ data_headers[each_value] + " " + list_of_data_types[each_value] + ", \n"
    create_query+="); \n \n"
    return create_query


def excel_data(request):
    if request.method == "POST":
        # var2 = request.FILES['excel_file'].name
        # table_name = request.POST.get('table_title')
        # table_schema_value = request.POST.get('table_schema_user_defined')
        # print(var2)
        excel_file = request.FILES["excel_file"]
        excel_sheet = request.POST.get('excel_sheet')
        excel_table_title = request.POST.get('excel_table_title')
        contain_header = request.POST['contain_header']
        excel_table_schema_user_defined = request.POST.get('excel_table_schema_user_defined')

        if excel_file:
            wb = openpyxl.load_workbook(excel_file)
            worksheet = wb[excel_sheet]
            # print(worksheet)

            excel_data = list()
            for row in worksheet.iter_rows():
                row_data = list()
                for cell in row:
                    if cell.value != None:
                        row_data.append(str(cell.value))
                excel_data.append(row_data)
            # print(excel_data)
        if contain_header == "Yes":
            headers = excel_data.pop(0)
        elif contain_header == "No":
            headers = [str(i) for i in range(len(excel_data[0]))]
        if excel_table_title and headers and excel_data:
            # print("excel_table_title ", excel_table_title)
            # print("headers ", headers)
            # print("excel_data ", excel_data)
            excel_table = excel_query_creation(headers, excel_data, excel_table_title)
            # cursor.execute(excel_table)
            # cursor.commit()
        if excel_table_schema_user_defined:
            tables_db = cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'dbo'")
            tables_lst = []  # TO GET FORMATTED TABLE NAMES
            for raw_table_names in tables_db:  # WILL OPT RAW DATA LIKE (TABLENAME,)
                for formatted_table_names in raw_table_names:
                    tables_lst.append(formatted_table_names)  # STORE FORMATTED NAMES OF TABLE
            # try:
            #     cursor.execute('DROP SCHEMA IF EXISTS ' + excel_table_schema_user_defined + ';')
            #     cursor.execute('CREATE SCHEMA ' + excel_table_schema_user_defined)
            #     for table_name in tables_lst:
            #         cursor.execute('ALTER SCHEMA ' + excel_table_schema_user_defined + ' TRANSFER dbo.' + table_name)
            #         cursor.commit()
            # except ProgrammingError:
            #     pass
            
        iterator_insert_query = "INSERT into " + excel_table_title  + " VALUES "
        count_checker = 0
        for each_list in range(len(excel_data)):
            iterator_insert_query+= "("
            for each_value in excel_data[each_list]:
                iterator_insert_query+= "'"+each_value+"',"
                        
                if iterator_insert_query[len(iterator_insert_query)-1] == ",":
                    print("-->", iterator_insert_query[len(iterator_insert_query)-1])
                    iterator_insert_query = iterator_insert_query[:len(iterator_insert_query)-1]
                    # print(iterator_insert_query[len(iterator_insert_query)-1])
                    # print("IF TRIGGERED")
                    # if count_checker == len(excel_data)-1: 
                    #     iterator_insert_query+=")"
                    # else:
                    #     iterator_insert_query+="), "
        # print(iterator_insert_query)

            #     if iterator_insert_query[len(iterator_insert_query)-1] == ",":
            #         iterator_insert_query = iterator_insert_query[:len(iterator_insert_query)-1]
            #         if count_checker == len(excel_data)-1: 
            #             iterator_insert_query+=")"
            #         else:
            #             iterator_insert_query+="), "
            #     if count_checker == len(excel_data)-1:
            #         iterator_insert_query+=";"
            #     else:
            #         count_checker+=1
        print(iterator_insert_query)
            
    return render(request, 'app_file/excel.html')



# def uploadTextEmail(request):
#     if request.method == "POST":
#         # var = request.POST.get('mytext')
#         var2 = request.FILES['myfile'].read().splitlines()
#         print(var2)
#         complete_query = ""
#         for i in var2:
#             temp = str(i)
#             temp2 = temp[1:]
#             complete_query+=temp2
#         print("\n", "Complete Query \n", complete_query)
#         t = complete_query.replace("'","\n")
#         t = t.replace('"',"")
#         print("\n T Query \n ", t)
#         # for i in query:
        #     print(i)

    
        #     complete_query+=str(i)[1:]
        # print("COMPLETED QUERY ", complete_query)
        # print(t)
        # s="SET IDENTITY_INSERT stores OFF INSERT INTO stores (store_name, phone, email, city) VALUES ('st1','12345','yasir@gmail.com','karachi')"
        # query = cursor.execute(s)
        # cursor.commit()
        # print("TRIGGERED")
        # for k in var2:
        #     complete_query+=str(k)[1:]
        #     print(k, type(k))
        #     print("complete_query --> ", complete_query)
        #     # print("str(k)[1:len(k)-4] --> ", str(k)[1:len(k)-4])
        #     print()
    # print()
    # print("complete_query", complete_query)
    # return render(request, "app_file/index.html")

# def updateEmail(request, emailid):
#     if request.method == 'GET':
#         updatedEmail = Marketer_Email.objects.get(id=emailid)
#         return render(request, 'updateemail.html')
#     else:
#         name = request.POST['name']
#         email = request.POST['email']
#         emailupdate = Marketer_Email.objects.get(id=emailid)
#         emailupdate.name = name
#         emailupdate.email = email
#         try:
#             emailupdate.save()
#         except:
#             print("NOT SAVE")
#         all_email =  Marketer_Email.objects.filter(userid=request.user.id)
#         return render(request, 'allemail.html', {'all_email': all_email})