# Generated by Django 4.2.6 on 2023-11-05 02:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lottery', '0019_alter_historydata_write_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historydata',
            name='write_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 5, 2, 54, 38, 522198)),
        ),
    ]
