# Generated by Django 2.0.1 on 2018-07-06 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exchange_core', '0046_auto_20180704_1720'),
    ]

    operations = [
        migrations.AddField(
            model_name='bankwithdraw',
            name='description',
            field=models.CharField(max_length=100, null=True, verbose_name='Description'),
        ),
        migrations.AddField(
            model_name='cryptowithdraw',
            name='description',
            field=models.CharField(max_length=100, null=True, verbose_name='Description'),
        ),
    ]
