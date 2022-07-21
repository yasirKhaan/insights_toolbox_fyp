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


