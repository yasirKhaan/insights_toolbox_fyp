from django.contrib import admin
from .models import table_column
from .models import graph_attributes
from .models import alarm_attributes
from .models import update_graphs

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

class alarm_attributes_Admin(admin.ModelAdmin):
    list_display = ['title', 'data_source', 'table_name', 'column_name', 'max', 'min', 'data', 'outlier']

admin.site.register(alarm_attributes, alarm_attributes_Admin)

class UpdateGraphsAdmin(admin.ModelAdmin):
    list_display = ('new_xaxis_schema',
                    'new_yaxis_schema',
                    'new_xaxis_table',
                    'new_yaxis_table',
                    'new_xaxis_column',
                    'new_yaxis_column',
                    'new_chart_title',
                    'new_plot_type',
                    'new_font_color',
                    'new_font_style',
                    'new_font_size',
                    'new_plot'
                    )

admin.site.register(update_graphs, UpdateGraphsAdmin)