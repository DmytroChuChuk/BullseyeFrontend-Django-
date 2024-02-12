# Generated by Django 4.2.6 on 2023-10-18 21:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lottery', '0009_alter_historydata_write_time'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userfavorite',
            old_name='lottery_id',
            new_name='lottery',
        ),
        migrations.RenameField(
            model_name='userfavorite',
            old_name='user_id',
            new_name='user',
        ),
        migrations.AlterField(
            model_name='historydata',
            name='write_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 18, 21, 53, 42, 612659)),
        ),
    ]