# Generated by Django 2.1.1 on 2018-09-17 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exchange_core', '0007_auto_20180917_2003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currencies',
            name='state',
            field=models.CharField(choices=[('active', 'Active'), ('inactive', 'Inativo')], default='active', max_length=30, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='historicalcurrencies',
            name='state',
            field=models.CharField(choices=[('active', 'Active'), ('inactive', 'Inativo')], default='active', max_length=30, verbose_name='Status'),
        ),
    ]
