from django.contrib import admin
from django.urls import path, include
from .views import mongo_data, sql_data

urlpatterns = [
    path('mongo-form/', mongo_data, name='mongo_form'),
    path('sql-form/', sql_data, name='sql-form')

]
