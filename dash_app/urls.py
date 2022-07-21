from django.urls import path

from . import views
from .views import report
from .views import send_gmail

urlpatterns = [
    path('analyze', views.index, name='analyze'),
    # path('try', views.try_view, name='try'),
    path('dashboard', views.dashboard, name='dashboard'),

    path('admin_data', views.admin_data, name='admin_data'),
    path('screenshot', views.screenshot, name='screenshot'),
    path('refresh_data', views.refresh_data, name='refresh'),

    path('connect', views.connect_db, name='connect'),
    path('csv', views.csv_connect, name='csv'),
    path('excel', views.excel_connect, name='excel'),
    path('nosql', views.nsql_connect, name='nosql'),
    path('sql', views.sql_connect, name='sql'),

    path('login', views.handleLogin, name='login'),
    path('signup', views.handleSignup, name='signup'),
    path('logout', views.handleLogout, name='logout'),

    path('home', views.home, name='home'),

    path('predict_form', views.predict_form, name='predict_form'),
    path('trainedmod', views.trainedmod, name='trainedmod'),
    path('final_prediction', views.final_prediction, name='final_prediction'),

    path('linreg', views.linearRegression, name='linreg'),
    path('logisreg', views.logisticRegression, name='logisreg'),

    path('report', views.report, name="report"),

    path('alarm', views.alarm, name="alarm"),
    path('alarm_manage', views.alarm_manage, name="alarm_manage"),

#ADMIN SIDE
    path('admin_alarm_manage', views.admin_alarm_manage, name="admin_alarm_manage"),
    path('delete/<int:pk>', views.deleteAction, name='delete'),

    path('admin_chart_manage', views.admin_chart_manage, name="admin_chart_manage"),
    path('delete_chart/<int:pk>', views.deleteAction_chart, name='delete_chart'),

    path('admin_dashboard', views.admin_dashboard, name='admin_dashboard'),



    path('send_mail/', send_gmail, name="send_mail"),



]