# Generated by Django 4.0.3 on 2023-10-17 18:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ActiveState',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(default='', max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='LotteryMetadata',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game', models.CharField(max_length=128)),
                ('number_of_balls', models.IntegerField()),
                ('ball_name', models.CharField(blank=True, max_length=128, null=True)),
                ('ball_min_value', models.IntegerField()),
                ('ball_max_value', models.IntegerField()),
                ('ball_allow_repeats', models.BooleanField(default=False)),
                ('ball_color', models.CharField(default=None, max_length=128, null=True)),
                ('number_of_special_balls', models.IntegerField(default=0)),
                ('special_ball_name', models.CharField(blank=True, default='', max_length=128, null=True)),
                ('special_ball_min_value', models.IntegerField(null=True)),
                ('special_ball_max_value', models.IntegerField(null=True)),
                ('special_ball_allow_repeats', models.BooleanField(default=False)),
                ('special_ball_color', models.CharField(default=None, max_length=128, null=True)),
                ('has_second_draw', models.BooleanField(default=False)),
                ('second_draw_name', models.CharField(default=None, max_length=128, null=True)),
                ('has_second_special_ball', models.BooleanField(default=False)),
                ('has_third_draw', models.BooleanField(default=False, null=True)),
                ('third_draw_name', models.CharField(default=None, max_length=128, null=True)),
                ('draw_times', models.CharField(max_length=128)),
                ('time_zone', models.CharField(max_length=128)),
                ('order_matters', models.BooleanField(default=False)),
                ('use_multiplier', models.BooleanField(default=False)),
                ('generate_special_balls', models.BooleanField(default=True)),
                ('users_sum', models.BooleanField(default=False)),
                ('track_jackpot', models.BooleanField(default=False, null=True)),
                ('number_of_balls_drawn', models.IntegerField(default=None, null=True)),
                ('reporting_delay_in_minutes', models.IntegerField(default=None, null=True)),
                ('skip_dates', models.TextField(default=None, null=True)),
                ('start_date', models.DateField(default=None, null=True)),
                ('last_result_date', models.DateField(default=None, null=True)),
                ('next_result_date', models.DateField(default=None, null=True)),
                ('next_result_datetime', models.DateTimeField(default=None, null=True)),
                ('link_to_game_site', models.CharField(max_length=256)),
                ('best_sum_min', models.IntegerField(default=None)),
                ('best_sum_max', models.IntegerField(default=None)),
                ('active_state', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='+', to='lottery.activestate')),
                ('country_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='lottery.country')),
            ],
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='UserFavorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lottery_id', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='+', to='lottery.lotterymetadata')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='lotterymetadata',
            name='state_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='lottery.state'),
        ),
    ]