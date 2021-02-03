# Generated by Django 3.0.8 on 2021-01-31 19:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapi', '0013_auto_20210124_0011'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='is_restaurant',
            field=models.BooleanField(blank=True, default=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='plannedDate',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='order',
            name='plannedTime',
            field=models.TimeField(default=datetime.time),
        ),
    ]
