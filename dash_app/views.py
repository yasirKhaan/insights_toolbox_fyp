import os.path
import random


from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import sklearn
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LinearRegression
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from .linreg import lin_reg_data_head, lin_reg_feature_selection, lin_reg_header, lin_reg_dimensions, lin_reg_r_value, lin_reg_intercept, lin_reg_predict, lin_reg_new_data
from .logisreg import data_head, header, feature_selection, data_dimension, data_nullable, train_test_data, predict, confusion_matrix, accuracy
from django import template
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from plotly.offline import plot
import plotly.graph_objects as go
from .forms import CreateUserForm
from .decorators import unauthenticated_user, func_to_allow, admins_only
import datetime
import pyodbc
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.core.mail import EmailMessage
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

from .models import table_column
from .models import graph_attributes
from .models import alarm_attributes
from .models import update_graphs

from .class_csv_connector import CsvConnection
from .excel_connector import ExcelConnection
from .class_nosql_connector import NoSQLConnection
from .class_sql_connector import SQLConnection
# from .screenshot import Screenshot

# from .sql_connector import create_tables_from_src_db, delete_tables, transfer_schema, data_into_primary_db
# from .nosql_connector import drop_tables, create_nsql_table, nsql_data_into_sql
# from .csv_connector import drop_csv_tables, csv_drop_schema, csv_to_sqltables, csvdata_to_sql
# from .excel_connector import drop_excel_tables, excel_drop_schema, excel_to_sqltables, exceldata_to_sql

conn_str = (
    r'DRIVER=ODBC Driver 17 for SQL Server;'
    r'SERVER=DESKTOP-2F5VLJ7;'
    r'DATABASE=maindatabase;'
    r'Trusted_Connection=yes;'
)
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()
# Create your views here.

def _input_field_query(col_name,schema_name,table_name):
    data = cursor.execute('SELECT '+col_name+' FROM '+schema_name+'.'+table_name)
    data_lst = []
    for rows in data:
        for formatted_schema in rows:
            data_lst.append(formatted_schema)
    return data_lst


def _all_schemas_of_db():
    data = cursor.execute('select TABLE_SCHEMA from INFORMATION_SCHEMA.TABLES;')
    data_lst = []
    for rows in data:
        for formatted_schema in rows:
            data_lst.append(formatted_schema)
    data_lst_set = set(data_lst)
    return data_lst_set

def _all_columns_of_db():

    sch_lst = []
    col_lst = []
    data = cursor.execute('SELECT TABLE_SCHEMA, TABLE_NAME FROM INFORMATION_SCHEMA.TABLES;')
    for tbl in data:
        sch_lst.append(list(tbl))

    for table in sch_lst:
        query = cursor.execute('SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '+"'"+table[1]+"'")
        col_lst_temp = []
        for col in query:
            for formatted_col in col:
                col_lst_temp.append(formatted_col)
        table_column.objects.create(schema_name = table[0], table_name=table[1], column_lst=col_lst_temp)
        col_lst.append(col_lst_temp)

    return sch_lst, col_lst


#ANALYZE SECTION

# @login_required(login_url='login')
# @func_to_allow(allowed_groups=['admins'])
# def index(request):
#     global xaxis_data_from_db
#     global yaxis_data_from_db
#     global xaxis_value_get
#     global yaxis_value_get
#     global graph_name_get
#     objects = None
#     xaxis_data_from_db = None
#     yaxis_data_from_db = None
#     x_schema = None
#     y_schema = None
#     graph_name_get = None
#     chart_title = None
#     font_style = None
#     font_color = None
#     font_size = None
#     all_schemas = _all_schemas_of_db()
#     all_columns = None
#     chart = None
#     chart_names = ['Scatter', 'Bar', 'Funnel', 'Box', 'Pie',]
#     labels_color = ['forestgreen', 'gold', 'grey', 'green','greenyellow', 'honeydew', 'khaki', 'lavender', 'lawngreen',
#                     'royalblue', 'saddlebrown', 'salmon', 'sandybrown','seagreen', 'seashell', 'sienna', 'silver','slategray', 'springgreen', 'steelblue', 'thistle',
#                     'tomato', 'violet', 'yellowgreen']
#     font_styles = ["Open Sherif", "Franklin Gothic","Arial","Times New Roman, monospace", 'Courier New, monospace']
#     font_size_range = [i for i in range(1,25)]
#     if request.method == "POST":
#         # COLUMNS
#         xaxis_value_get = request.POST.get('xaxis') # FIRSTNAME
#         yaxis_value_get = request.POST.get('yaxis') # LASTNAME
#         # GRAPH
#         graph_name_get = request.POST['graph_type'] # FIRSTNAME
#         # SCHEMAS
#         x_schema = request.POST['xaxis_schema']
#         y_schema = request.POST['yaxis_schema']
#         # TABLES
#         x_table = request.POST.get('xaxis_table')
#         y_table = request.POST.get('yaxis_table')
#         # GET VALUES FROM DB
#         xaxis_data_from_db = _input_field_query(xaxis_value_get, x_schema, x_table)
#         yaxis_data_from_db = _input_field_query(yaxis_value_get, y_schema, y_table)
#
#         # FORMATTING SECTIOM
#         chart_title = request.POST.get('chart_title')
#         font_color = request.POST['font_color']
#         font_style = request.POST['font_style']
#         font_size = int(request.POST['font_size'])
#         # all_columns = _all_columns_of_db()
#         chart = try_view(xaxis_data_from_db, yaxis_data_from_db, graph_name_get, chart_title, font_color, font_style, font_size)
#
#         # objects = table_column.objects.all()
#         graph_attributes.objects.create(xaxis_schema=x_schema,
#                                         yaxis_schema=y_schema,
#                                         xaxis_table=x_table,
#                                         yaxis_table=y_table,
#                                         xaxis_column=xaxis_value_get,
#                                         yaxis_column=yaxis_value_get,
#                                         chart_title=chart_title,
#                                         font_color=font_color,
#                                         font_style=font_style,
#                                         font_size=font_size,
#                                         plot=chart,
#                                         plot_type=graph_name_get
#                                         )
#
#     objects = table_column.objects.all()
#
#     context = {
#         'fetched_data_x': xaxis_data_from_db,
#         'fetched_data_y': yaxis_data_from_db,
#         'schemas': all_schemas,
#         'chart_styles': chart_names,
#         'font_colors': labels_color,
#         'font_styles': font_styles,
#         'font_range': font_size_range,
#         'plot1': chart,
#         'abc': objects
#     }
#
#     return render(request, 'dash_app/analyze.html',context)

@login_required(login_url='login')
@func_to_allow(allowed_groups=['admins'])
def index(request):
    global xaxis_data_from_db
    global yaxis_data_from_db
    global xaxis_value_get
    global yaxis_value_get
    global graph_name_get
    global x_table
    Objects = table_column.objects.all()
    xaxis_data_from_db = None
    yaxis_data_from_db = None
    x_schema = None
    y_schema = None
    graph_name_get = None
    chart_title = None
    font_style = None
    font_color = None
    font_size = None
    all_schemas = _all_schemas_of_db()
    all_columns = None
    chart = None
    chart_names = ['Scatter', 'Bar', 'Funnel', 'Box', 'Pie',]
    labels_color = ['forestgreen', 'gold', 'grey', 'green','greenyellow', 'honeydew', 'khaki', 'lavender', 'lawngreen',
                    'royalblue', 'saddlebrown', 'salmon', 'sandybrown','seagreen', 'seashell', 'sienna', 'silver','slategray', 'springgreen', 'steelblue', 'thistle',
                    'tomato', 'violet', 'yellowgreen']
    font_styles = ["Open Sherif", "Franklin Gothic","Arial","Times New Roman, monospace", 'Courier New, monospace']
    font_size_range = [i for i in range(1,25)]
    if request.method == "POST":
        # COLUMNS
        xaxis_value_get = request.POST.get('xaxis') # FIRSTNAME
        yaxis_value_get = request.POST.get('yaxis') # LASTNAME
        # GRAPH
        graph_name_get = request.POST['graph_type'] # FIRSTNAME
        # SCHEMAS
        x_schema = request.POST['xaxis_schema']
        y_schema = request.POST['yaxis_schema']
        # TABLES
        x_table = request.POST.get('xaxis_table')
        y_table = request.POST.get('yaxis_table')
        # GET VALUES FROM DB
        xaxis_data_from_db = _input_field_query(xaxis_value_get, x_schema, x_table)
        yaxis_data_from_db = _input_field_query(yaxis_value_get, y_schema, y_table)
        # FORMATTING SECTIOM
        chart_title = request.POST.get('chart_title')
        font_color = request.POST['font_color']
        font_style = request.POST['font_style']
        font_size = int(request.POST['font_size'])
        # all_columns = _all_columns_of_db()
        chart = try_view(xaxis_data_from_db, yaxis_data_from_db, graph_name_get, chart_title, font_color, font_style, font_size,xaxis_value_get, yaxis_value_get)

        # objects = table_column.objects.all()
        graph_attributes.objects.create(xaxis_schema=x_schema,
                                        yaxis_schema=y_schema,
                                        xaxis_table=x_table,
                                        yaxis_table=y_table,
                                        xaxis_column=xaxis_value_get,
                                        yaxis_column=yaxis_value_get,
                                        chart_title=chart_title,
                                        font_color=font_color,
                                        font_style=font_style,
                                        font_size=font_size,
                                        plot=chart,
                                        plot_type=graph_name_get
                                        )
        update_graphs.objects.create(new_xaxis_schema=x_schema,
                                     new_yaxis_schema=y_schema,
                                     new_xaxis_table=x_table,
                                     new_yaxis_table=y_table,
                                     new_xaxis_column=xaxis_value_get,
                                     new_yaxis_column=yaxis_value_get,
                                     new_chart_title=chart_title,
                                     new_font_color=font_color,
                                     new_font_style=font_style,
                                     new_font_size=font_size,
                                     new_plot=chart,
                                     new_plot_type=graph_name_get
                                     )
        # Objects = table_column.objects.all()

    context = {
        'fetched_data_x': xaxis_data_from_db,
        'fetched_data_y': yaxis_data_from_db,
        'schemas': all_schemas,
        'chart_styles': chart_names,
        'font_colors': labels_color,
        'font_styles': font_styles,
        'font_range': font_size_range,
        'plot1': chart,
        'abc': Objects
    }



    return render(request, 'dash_app/analyze.html',context)


# def try_view(xaxis, yaxis, graph_style, chart_title, font_color, font_style, font_size):
#
#
#     x1 = xaxis
#     y1 = yaxis
#     trace = None
#     trace1 = None
#     if graph_style.lower() == 'scatter':
#         trace = go.Scatter(
#             x=x1,
#             y=y1,
#             name='TEST'
#         )
#
#     if graph_style.lower() == 'box':
#         trace = go.Box(
#             x=x1,
#             y=y1
#         )
#
#     if graph_style.lower() == 'bar':
#         trace = go.Bar(
#             x=x1,
#             y=y1
#         )
#
#     if graph_style.lower() == 'pie':
#         trace = go.Pie(
#             values=x1,
#             labels=y1,
#
#             hoverinfo="label+percent+name",
#         )
#
#     if graph_style.lower() == 'funnel':
#         trace = go.Funnel(
#             x=x1,
#             y=y1,
#
#         )
#
#
#     layout = dict(
#         title=chart_title,
#         xaxis=dict(range=[min(x1), max(x1)]),
#         yaxis=dict(range=[min(y1), max(y1)]),
#     )
#
#     if type(font_color) == str:
#         temp_color = font_color
#     fig = go.Figure(data=trace, layout=layout)
#     fig.update_layout(
#         xaxis_title= xaxis_value_get,
#         yaxis_title=yaxis_value_get,
#         font=dict(
#             family=font_style,
#             size=font_size,
#             color=font_color
#         )
#     )
#     fig.update_layout(title_text=chart_title, title_x=0.5)
#
#     plot_div = plot(fig, output_type='div', include_plotlyjs=False)
#
#     return plot_div

def try_view(xaxis, yaxis, graph_style, chart_title, font_color, font_style, font_size, x_col_name, y_col_name):


    x1 = xaxis
    y1 = yaxis
    trace = None
    trace1 = None
    if graph_style.lower() == 'scatter':
        trace = go.Scatter(
            x=x1,
            y=y1,
            name='TEST'
        )

    if graph_style.lower() == 'box':
        trace = go.Box(
            x=x1,
            y=y1
        )

    if graph_style.lower() == 'bar':
        trace = go.Bar(
            x=x1,
            y=y1
        )

    if graph_style.lower() == 'pie':
        trace = go.Pie(
            values=x1,
            labels=y1,

            hoverinfo="label+percent+name",
        )

    if graph_style.lower() == 'funnel':
        trace = go.Funnel(
            x=x1,
            y=y1,

        )


    layout = dict(
        title=chart_title,
        xaxis=dict(range=[min(x1), max(x1)]),
        yaxis=dict(range=[min(y1), max(y1)]),
    )

    if type(font_color) == str:
        temp_color = font_color
    fig = go.Figure(data=trace, layout=layout)
    fig.update_layout(
        xaxis_title= x_col_name,
        yaxis_title=y_col_name,
        font=dict(
            family=font_style,
            size=int(font_size),
            color=font_color
        )
    )
    fig.update_layout(title_text=chart_title, title_x=0.5)

    plot_div = plot(fig, output_type='div', include_plotlyjs=False)

    return plot_div


#DASHBOARD SECTION

def refresh_data(request):
    update_graphs.objects.all().delete()
    objects = graph_attributes.objects.all()
    lst_charts = []
    for each in objects:
        new_xaxis_data_from_db = _input_field_query(each.xaxis_column, each.xaxis_schema, each.xaxis_table)
        new_yaxis_data_from_db = _input_field_query(each.yaxis_column, each.yaxis_schema, each.yaxis_table)
        chart = try_view(new_xaxis_data_from_db, new_yaxis_data_from_db, each.plot_type, each.chart_title,
                         each.font_color, each.font_style, each.font_size, each.xaxis_table, each.yaxis_table)
        # print(new_xaxis_data_from_db)
        # print()
        # print(new_yaxis_data_from_db)
        lst_charts.append(chart)
        update_graphs.objects.create(new_xaxis_schema=each.xaxis_schema,
                                     new_yaxis_schema=each.yaxis_schema,
                                     new_xaxis_table=each.xaxis_table,
                                     new_yaxis_table=each.yaxis_table,
                                     new_xaxis_column=each.xaxis_column,
                                     new_yaxis_column=each.yaxis_column,
                                     new_chart_title=each.chart_title,
                                     new_font_color=each.font_color,
                                     new_font_style=each.font_style,
                                     new_font_size=each.font_size,
                                     new_plot=chart,
                                     new_plot_type=each.plot_type
                                     )

    print('** SQL **')
    sqlobj = SQLConnection('ODBC Driver 17 for SQL Server','(local)','firstdb','SQL')
    sqlobj.create_tables_from_src_db()
    sqlobj.delete_tables()
    sqlobj.create_tables_from_src_db()
    sqlobj.transfer_schema()
    sqlobj.data_into_primary_db()

    #mongo
    print('** MONGO **')
    nsqlobj = NoSQLConnection('mongodb://localhost:27017/first_db_nsql','first_db_nsql','nsql_table','NOSQL')
    nsqlobj.drop_tables()
    nsqlobj.nsql_to_sql_tables()
    nsqlobj.nsql_data_to_sql()

    #csv

    print('** CSV **')
    csv = CsvConnection(r'C:\\Users\\KHURRAM\\Downloads\\sample dataset\\SAMPLECSV.csv','CSV','csv_table')
    csv.drop_csv_tables()
    csv.csv_drop_schema()
    csv.csv_to_sqltables()
    csv.csvdata_to_sql()



    objects = graph_attributes.objects.all()

    updated_graphs_objects = update_graphs.objects.all()
    context = {
        'demo': [1, 2, 3],
        'upt_graphs': updated_graphs_objects

    }
    return render(request, 'dash_app/refresh.html', context)

# def dashboard(request):
#
#     objects = graph_attributes.objects.all()
#     context = {
#         'graph' : objects
#     }
#
#     return render(request, 'dash_app/canvas.html', context)

def dashboard(request):

    # _all_columns_of_db()
    updated_graph_objs = graph_attributes.objects.all()
    updated_graph_objs1 = update_graphs.objects.all()

    context = {
        'graph' : updated_graph_objs
    }

    return render(request, 'dash_app/canvas.html', context)

#ALL DATA CONNECTION SECTION

def csv_connect(request):

    csv_path = None
    schema_name = None
    table_name = None
    if request.method == "POST":
        csv_path = request.POST.get('csv_path')
        schema_name = request.POST.get('schema_name')
        table_name = request.POST.get('table_name')
        # var = 'C:\\Users\\KHURRAM\\Downloads\\sample dataset\\SAMPLECSV.csv'
        csv = CsvConnection(csv_path, schema_name, table_name)
        csv.get_column()
        csv.create_schema()
        csv.csv_to_sqltables()
        csv.csvdata_to_sql()

    context = {
        'message' : 'CSV SUCCESFULLY CONNECTED'
    }
    return render(request, 'dash_app/csv_connect.html',context)

def excel_connect(request):

    excel_path = None
    schema_name = None
    table_name = None
    if request.method == "POST":
        excel_path = request.POST.get('excel_path')
        schema_name = request.POST.get('schema_name')
        table_name = request.POST.get('table_name')
        # var = 'C:\\Users\\KHURRAM\\Downloads\\sample dataset\\SAMPLECSV.csv'
        excel = ExcelConnection(excel_path, schema_name, table_name)
        excel.get_column()
        excel.excel_to_sqltables()
        excel.exceldata_to_sql()

    context = {
        'message' : 'EXCEL SUCCESFULLY CONNECTED'
    }
    return render(request, 'dash_app/excel_connect.html',context)

def nsql_connect(request):
    nosql_str = None
    db_name = None
    table_name = None
    datasource_name = None
    if request.method == "POST":
        nosql_str = request.POST.get('nosql_str')
        # db_name = request.POST.get('db_name')
        db_name = 'first_db_nsql'
        table_name = request.POST.get('table_name')
        datasource_name = request.POST.get('datasource_name')
        # var = 'C:\\Users\\KHURRAM\\Downloads\\sample dataset\\SAMPLECSV.csv'
        nsql = NoSQLConnection(nosql_str, db_name, table_name, datasource_name)
        nsql.get_keys_in_lst()
        nsql.nsql_to_sql_tables()
        nsql.nsql_data_to_sql()

    context = {
        'message' : 'NO-SQL SUCCESFULLY CONNECTED'
    }
    return render(request, 'dash_app/nosql_connect.html',context)

def sql_connect(request):
    driver = None
    server = None
    db_name = None
    datasource_name = None
    if request.method == "POST":
        driver = request.POST.get('driver')
        server = request.POST.get('server')
        db_name = request.POST.get('db_name')
        datasource_name = request.POST.get('datasource_name')
        sql = SQLConnection(driver, server, db_name, datasource_name)

        sql.create_tables_from_src_db()
        sql.transfer_schema()
        sql.data_into_primary_db()


    context = {
        'message' : 'SQL SUCCESFULLY CONNECTED'
    }
    return render(request, 'dash_app/sql_connect.html',context)




def handleSignup(request):
    if request.user.is_authenticated:
        return redirect('analyze')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user = form.save()
                username = form.cleaned_data.get('username')
                group = Group.objects.get(name='customers')
                user.groups.add(group)
                messages.success(request,'Account Created Successfully For ' + username)
                return redirect('login')

        context={'form': form}
        return render(request, 'dash_app/signup.html', context)


@unauthenticated_user
def handleLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Incorrect Information')
    context={}
    return render(request, 'dash_app/login.html', context)


def handleLogout(request):
    logout(request)
    return redirect('login')

def home(request):

    context = {}
    return render(request, 'dash_app/home.html', context)

#CONNECT PHASE

def connect_db(request):

    context = {}
    return render(request, 'dash_app/connect.html', context)

def linearRegression(request):
    context = {
        'data_head': lin_reg_data_head(),
        'data_headers': lin_reg_header(),
        'features': lin_reg_feature_selection(),
        'data_dim': lin_reg_dimensions(),
        'rsq_value': lin_reg_r_value(),
        'intercept': lin_reg_intercept(),
        'lin_reg_new_data_pred': lin_reg_new_data(),
        'lin_reg_prediction': lin_reg_predict(),

    }
    return render(request, 'dash_app/linreg.html', context)

def logisticRegression(request):
    context = {
        'data_head': data_head(),
        'data_headers': header(),
        'features': feature_selection(),
        'data_dim': data_dimension(),
        'nullable': data_nullable(),
        'train_data': train_test_data(),
        'predict': predict(),
        'matrix': confusion_matrix(),
        'accuracy': accuracy(),
    }
    return render(request, 'dash_app/logisreg.html', context)


#REPORT SECTION

def screenshot(request):
    global shotname
    if request.method == "POST":
        shotname = str(random.randint(0, 10000))
        options = webdriver.ChromeOptions()
        options.headless = True
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.implicitly_wait(10)

        # driver.get('http://127.0.0.1:8000/dashboard')
        #     driver.get('https://www.lipsum.com/')
        driver.get('C:/Users/KHURRAM/Desktop/Lorem.html')

        S = lambda X: driver.execute_script('return document.body.parentNode.scroll' + X)
        driver.set_window_size(S('Width'), S('Height'))

        dir_name = 'C:/Users/KHURRAM/PycharmProjects/fyp-dashboard/static/report'
        base_filename = shotname
        suffix = '.png'

        path = os.path.join(dir_name, base_filename + suffix)

        driver.find_element(By.TAG_NAME, 'body').screenshot(path)

        url = 'report'
        resp_body = '<script>alert("CURRENT REPORT PULLED AND SAVED!");\
                     window.location="%s"</script>' % url
        return HttpResponse(resp_body)

def report(request):
    return render(request, 'dash_app/report.html')

def send_gmail(request):
    subject = None
    message = None
    if request.method == "POST":
        name = request.POST.get('name')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        email = request.POST.get('email')
        message = "REPORT NAME : " + name + "\n" + message

        email = EmailMessage(subject,
                             message,
                             'insightstoolboxfyp@gmail.com',
                             [email]
                             )

        dir_name = 'C:/Users/KHURRAM/PycharmProjects/fyp-dashboard/static/report'
        base_filename = shotname
        suffix = '.png'

        path = os.path.join(dir_name, base_filename + suffix)
        # email.attach_file('C:\\Users\\KHURRAM\\PycharmProjects\\fyp-dashboard\\dash_app\\fyp_logo.jpeg')

        email.attach_file(path)
        email.send(fail_silently=False)

        return HttpResponseRedirect(reverse('report'))
    else:
        return HttpResponse('Invalid request')

#ALARM SECTION

def alarm(request):
    global data_from_db
    data_from_db = None
    max = None
    min = None
    data_lst = []
    outlier_lst = []

    if request.method == "POST":
        title = request.POST.get('title')
        data_source = request.POST.get('datasource')
        table_name = request.POST.get('table_name')
        column_name = request.POST.get('column_name')
        max = int(request.POST.get('max'))
        min = int(request.POST.get('min'))


        query = cursor.execute(
            'SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = ' + "'" + table_name + "'")
        col_lst_temp = []
        for col in query:
            for formatted_col in col:
                col_lst_temp.append(formatted_col)


        index = None
        if column_name in col_lst_temp:
            index = col_lst_temp.index(column_name)

        datatype = []
        query = cursor.execute(
            "SELECT frs.system_type_name FROM sys.dm_exec_describe_first_result_set(" + "'select top 10 * from " + data_source + "." + table_name + "',NULL,NULL) frs;")
        for i in query:
            for j in i:
                datatype.append(j)


        if datatype[index] == "int":
            pass
            range_lst = []
            for i in range(min, max + 1):
                range_lst.append(i)

            data = cursor.execute('SELECT * FROM '+data_source+'.'+table_name+';')
            for rows in data:
                if rows[index] in range_lst:
                    data_lst.append(rows)
                else:
                    outlier_lst.append(rows)

            alarm_attributes.objects.create(title=title,
                                            data_source=data_source,
                                            table_name=table_name,
                                            column_name=column_name,
                                            max=max,
                                            min=min,
                                            data=data_lst,
                                            outlier=outlier_lst
                                            )


        else:
            print(" ENTER THE INTEGER COLUMN ONLY ")

    objects = table_column.objects.all()

    context = {
        'fetched_data': data_lst,
        'outlier': outlier_lst,
        'max_value' : max,
        'min_value' : min,
        'abc': objects
    }

    return render(request,'dash_app/alarm.html',context)

def alarm_manage(request):

    objects = alarm_attributes.objects.all()

    context ={
        'obj' : objects
    }
    return render(request,'dash_app/alarm_manage.html',context)

#ADMIN PANEL SECTION

def admin_alarm_manage(request):

    objects = alarm_attributes.objects.all()
    context ={
        'list' : objects
    }
    return render(request,'dash_app/admin_alarm_manage.html',context)

#ALARM DELETING
def deleteAction(request, pk):
    pickTodo = alarm_attributes.objects.get(pk=pk)
    pickTodo.delete()
    return redirect('admin_alarm_manage')

def admin_chart_manage(request):

    objects = graph_attributes.objects.all()
    context ={
        'list' : objects
    }
    return render(request,'dash_app/admin_chart_manage.html',context)

#CHART DELETING
def deleteAction_chart(request, pk):
    pickTodo = graph_attributes.objects.get(pk=pk)
    pickTodo.delete()
    return redirect('admin_chart_manage')

def admin_dashboard(request):
    return render(request, 'dash_app/admin_dashboard.html')

#ALL DATA INFORMATION
def admin_data(request):
    context = {
        'list': table_column.objects.all()
    }
    return render(request, 'dash_app/admin_data.html', context)

def predict_form(request):
    global ind_var_dict
    ind_var_dict = {
        'column_name':[],
        'quantity': [],
    }
    if request.method == "POST":
        global get_model
        #get_xtext = request.POST.get('x_axis')
        #print(get_xtext)
        x_axis=eval(request.POST.get("x_axis"))
        x_axis=[i["value"] for i in x_axis]
        #print(x_axis)
        get_ytext = request.POST.get('y_axis')
        get_model= request.POST.get('model')
        get_data_source= request.POST.get('data_source')
        df =pd.read_csv('Iris.csv')
        if get_data_source == 'csv':
            df =pd.read_csv('Iris.csv')
        if get_data_source == 'excel':
            df =pd.read_excel('excel_db.xlsx')

        df_x=df[x_axis]
        df_y=df[get_ytext]
        for columns in x_axis:
            ind_var_dict['column_name'].append(columns)
            ind_var_dict['quantity'].append(1)

        print('*** x_axis ***')
        print(ind_var_dict)

        if get_model == '1':
            global lin_reg
            global model1
            df_x.values.reshape(-1, 1)
            df_y.values.reshape(-1, 1)
            X_train, X_test, y_train, y_test=train_test_split(df_x,df_y, test_size=float(request.POST.get('test')),random_state=1)
            #c1met=col1.values.reshape(-1,1)
            model1=LinearRegression()
            global s
            lin_reg = model1.fit(X_train, y_train)
            predicted1 = model1.predict(X_test)
            # print(model1)
            # print(lin_reg)
            # print("Predicted Value of Linear Regression is",predicted1)
        if get_model == '2':
            global model2
            X_train, X_test, y_train, y_test=train_test_split(df_x,df_y, test_size=float(request.POST.get('test')),random_state=1)
            df_x.values.reshape(-1, 1)
            model2 = LogisticRegression()
            model2.fit(X_train, y_train)
            # print('processing')
            predicted2=model2.predict(X_test)
            # print("PREDICTED VALUE IS",predicted2)

            #score=model2.score(x,y)
            #print(score)

    model_trained_head = "MODEL TRAINED SUCCESSFULLY"
    context={
        'mod_head' : model_trained_head,
    }

    return render(request, 'dash_app/predict_form.html', context)

def trainedmod(request):
    if request.method == "POST":
        global ind_var_vals
        ind_var_vals = []
        ud_vals = eval(request.POST.get("ud_vals"))
        ud_vals = [(s["value"]) for s in ud_vals]
        print(ud_vals)
        ind_var_vals.append(ud_vals)
    return render(request, 'dash_app/trainedmod.html')


def final_prediction(request):
    lin_reg=None
    log_reg=None
    if get_model == '1':
        lin_reg = model1.predict(ind_var_vals)
    if get_model == '2':
        log_reg = model2.predict(ind_var_vals)
    # 1, 5.1, 3.5, 1.4, 0.2,
    # data = pd.DataFrame(data=[5.1],columns=['a'])
    # data.reshape(1, -1)
    # print(lin_reg)
    # print("ind_var_vals")
    # print(ind_var_vals)
    print(get_model)

    context={
        'key_pred': lin_reg,
        'log_pred': log_reg,
        'model_selection': get_model
    }
    return render(request, 'dash_app/final_prediction.html', context)

