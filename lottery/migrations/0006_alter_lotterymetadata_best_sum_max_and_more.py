# Generated by Django 4.0.3 on 2023-10-18 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lottery', '0005_rename_users_sum_lotterymetadata_uses_sum'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lotterymetadata',
            name='best_sum_max',
            field=models.IntegerField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='lotterymetadata',
            name='best_sum_min',
            field=models.IntegerField(default=None, null=True),
        ),
    ]