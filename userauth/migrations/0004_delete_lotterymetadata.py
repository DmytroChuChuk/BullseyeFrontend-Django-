# Generated by Django 4.2.6 on 2023-10-13 22:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userauth', '0003_lotterymetadata'),
    ]

    operations = [
        migrations.DeleteModel(
            name='LotteryMetadata',
        ),
    ]
