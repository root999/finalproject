# Generated by Django 3.0.8 on 2020-12-26 20:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapi', '0002_restaurant'),
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('restaurant', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='myapi.Restaurant')),
                ('products', models.ManyToManyField(blank=True, related_name='menus', to='myapi.Product')),
            ],
        ),
    ]
