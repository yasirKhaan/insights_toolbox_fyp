"""file_reader URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from app_file.views import data_update, mongo_data, sql_data, csv_data, excel_data

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', mongo_data, name='home_file'),
    path('sql/', sql_data, name='sql-form'),
    path('csv/', csv_data, name='sql-form'),
    path('excel/', excel_data, name='sql-form'),
    path('data/', data_update, name='sql-form')

    # path('file/', include('app_file.urls')),
    

]
