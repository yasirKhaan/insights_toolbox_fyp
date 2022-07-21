from django.db import models

# Create your models here.

class table_column(models.Model):
    schema_name = models.TextField()
    table_name = models.TextField()
    column_lst = models.TextField()


class graph_attributes(models.Model):

    xaxis_schema = models.TextField()
    yaxis_schema = models.TextField()

    xaxis_table = models.TextField()
    yaxis_table = models.TextField()

    xaxis_column = models.TextField()
    yaxis_column= models.TextField()

    plot_type = models.TextField()
    plot = models.TextField()


    chart_title = models.TextField()
    font_color = models.TextField()
    font_style = models.TextField()
    font_size = models.TextField()

class alarm_attributes(models.Model):
    title = models.TextField()
    data_source = models.TextField()
    table_name = models.TextField()
    column_name = models.TextField()
    max = models.IntegerField()
    min = models.TextField()
    data = models.TextField()
    outlier = models.TextField()

class update_graphs(models.Model):

    new_xaxis_schema = models.TextField()
    new_yaxis_schema = models.TextField()

    new_xaxis_table = models.TextField()
    new_yaxis_table = models.TextField()

    new_xaxis_column = models.TextField()
    new_yaxis_column= models.TextField()

    new_plot_type = models.TextField()
    new_plot = models.TextField()


    new_chart_title = models.TextField()
    new_font_color = models.TextField()
    new_font_style = models.TextField()
    new_font_size = models.TextField()


