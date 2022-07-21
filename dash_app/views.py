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
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import table_column
from .models import graph_attributes

from .class_csv_connector import CsvConnection
from .excel_connector import ExcelConnection
from .class_nosql_connector import NoSQLConnection
from .class_sql_connector import SQLConnection

conn_str = (
    r'DRIVER=ODBC Driver 17 for SQL Server;'
    r'SERVER=DESKTOP-2F5VLJ7;'
    r'DATABASE=milestone;'
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
#
# _all_columns_of_db()


@login_required(login_url='login')
@func_to_allow(allowed_groups=['admins'])
def index(request):
    global xaxis_data_from_db
    global yaxis_data_from_db
    global xaxis_value_get
    global yaxis_value_get
    global graph_name_get
    objects = None
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
        chart = try_view(xaxis_data_from_db, yaxis_data_from_db, graph_name_get, chart_title, font_color, font_style, font_size)

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

    objects = table_column.objects.all()

    context = {
        'fetched_data_x': xaxis_data_from_db,
        'fetched_data_y': yaxis_data_from_db,
        'schemas': all_schemas,
        'chart_styles': chart_names,
        'font_colors': labels_color,
        'font_styles': font_styles,
        'font_range': font_size_range,
        'plot1': chart,
        'abc': objects
    }



    return render(request, 'dash_app/analyze.html',context)


def try_view(xaxis, yaxis, graph_style, chart_title, font_color, font_style, font_size):


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
        xaxis_title= xaxis_value_get,
        yaxis_title=yaxis_value_get,
        font=dict(
            family=font_style,
            size=font_size,
            color=font_color
        )
    )
    fig.update_layout(title_text=chart_title, title_x=0.5)

    plot_div = plot(fig, output_type='div', include_plotlyjs=False)

    return plot_div


def sample(request):

    # _all_columns_of_db()

    objects = table_column.objects.all()

    # instance = table_column.objects.values('schema_name')
    # value = instance[0]['schema_name']
    # # print(instance)
    #
    # return HttpResponse(value)

    context = {
        'abc' : objects
    }

    return render(request, 'dash_app/sample.html', context)

#
# xaxis_data_from_db = None
# yaxis_data_from_db = None


def dashboard(request):

    # _all_columns_of_db()

    objects = graph_attributes.objects.all()

    context = {
        'graph' : objects
    }

    return render(request, 'dash_app/canvas.html', context)

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

def report(request):
    return render(request,'dash_app/report.html')

def send_gmail(request):
    name=None
    subject=None
    message = None
    if request.method=="POST":
        name = request.POST.get('name')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        email = request.POST.get('email')
        print(name, subject, message, email)

        send_mail(
            subject,
            message,
            'insightstoolboxfyp@gmail.com',
            [email],
            fail_silently=False,
        )

        return HttpResponseRedirect(reverse('report'))
    else:
        return HttpResponse('Invalid request')
