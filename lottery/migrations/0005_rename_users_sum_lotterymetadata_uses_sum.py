# Generated by Django 4.0.3 on 2023-10-18 16:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lottery', '0004_rename_country_id_lotterymetadata_country_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lotterymetadata',
            old_name='users_sum',
            new_name='uses_sum',
        ),
    ]