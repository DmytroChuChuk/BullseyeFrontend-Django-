# Generated by Django 4.0.3 on 2023-10-18 15:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lottery', '0003_alter_activestate_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lotterymetadata',
            old_name='country_id',
            new_name='country',
        ),
        migrations.RenameField(
            model_name='lotterymetadata',
            old_name='state_id',
            new_name='state',
        ),
    ]
