# Generated by Django 4.0.3 on 2023-10-17 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lottery', '0002_alter_activestate_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activestate',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
