from django.urls import path

from . import views
from .views import report
from .views import send_gmail

urlpatterns = [
    path('analyze', views.index, name='analyze'),
    # path('try', views.try_view, name='try'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('sample', views.sample, name='sample'),

    path('connect', views.connect_db, name='connect'),
    path('csv', views.csv_connect, name='csv'),
    path('excel', views.excel_connect, name='excel'),
    path('nosql', views.nsql_connect, name='nosql'),
    path('sql', views.sql_connect, name='sql'),

    path('login', views.handleLogin, name='login'),
    path('signup', views.handleSignup, name='signup'),
    path('logout', views.handleLogout, name='logout'),

    path('home', views.home, name='home'),

    path('linreg', views.linearRegression, name='linreg'),
    path('logisreg', views.logisticRegression, name='logisreg'),

    path('', report, name="report"),
    path('send_mail/', send_gmail, name="send_mail"),



]