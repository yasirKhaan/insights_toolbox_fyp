from django.contrib import admin
from .models import table_column
from .models import graph_attributes

# Register your models here.
class table_column_Admin(admin.ModelAdmin):
    list_display = ['schema_name', 'table_name', 'column_lst']

admin.site.register(table_column, table_column_Admin)


class graph_attributes_Admin(admin.ModelAdmin):
    list_display = ['xaxis_schema',
                    'yaxis_schema',
                    'xaxis_table',
                    'yaxis_table',
                    'xaxis_column',
                    'yaxis_column',
                    'chart_title',
                    'plot_type',
                    'font_color',
                    'font_style',
                    'font_size',
                    'plot'
                    ]

admin.site.register(graph_attributes, graph_attributes_Admin)