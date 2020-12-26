# Generated by Django 3.0.8 on 2020-12-26 20:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapi', '0003_menu'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('surname', models.CharField(max_length=50)),
            ],
        ),
        migrations.AlterField(
            model_name='menu',
            name='products',
            field=models.ManyToManyField(blank=True, to='myapi.Product'),
        ),
        migrations.AlterField(
            model_name='menu',
            name='restaurant',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='menu', serialize=False, to='myapi.Restaurant'),
        ),
    ]
