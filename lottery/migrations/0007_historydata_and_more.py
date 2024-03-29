# Generated by Django 4.0.3 on 2023-10-18 17:55

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lottery', '0006_alter_lotterymetadata_best_sum_max_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoryData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=None)),
                ('balls', models.CharField(max_length=256, null=True)),
                ('spacial_balls', models.CharField(max_length=256, null=True)),
                ('second_draw_balls', models.CharField(max_length=256, null=True)),
                ('second_draw_special_balls', models.CharField(max_length=256, null=True)),
                ('third_draw_balls', models.CharField(max_length=256, null=True)),
                ('multiplier', models.CharField(max_length=16, null=True)),
                ('jackpot', models.CharField(max_length=64, null=True)),
                ('write_time', models.DateTimeField(default=datetime.datetime(2023, 10, 18, 17, 55, 39, 627200))),
                ('lottery', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='+', to='lottery.lotterymetadata')),
            ],
        ),
        migrations.AddConstraint(
            model_name='historydata',
            constraint=models.UniqueConstraint(fields=('lottery', 'date'), name='unique_lottery_date_combination'),
        ),
    ]
