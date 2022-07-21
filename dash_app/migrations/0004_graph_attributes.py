# Generated by Django 4.0.1 on 2022-01-31 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dash_app', '0003_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='graph_attributes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('xaxis_schema', models.TextField()),
                ('yaxis_schema', models.TextField()),
                ('xaxis_table', models.TextField()),
                ('yaxis_table', models.TextField()),
                ('xaxis_column', models.TextField()),
                ('yaxis_column', models.TextField()),
                ('chart_title', models.TextField()),
                ('font_color', models.TextField()),
                ('font_style', models.TextField()),
                ('font_size', models.TextField()),
            ],
        ),
    ]
