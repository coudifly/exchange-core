# Generated by Django 2.0.2 on 2018-02-06 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exchange_core', '0011_auto_20180204_1555'),
    ]

    operations = [
        migrations.AddField(
            model_name='statement',
            name='tx_id',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]