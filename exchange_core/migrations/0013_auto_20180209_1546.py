# Generated by Django 2.0.1 on 2018-02-09 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exchange_core', '0012_statement_tx_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='bankwithdraw',
            name='tx_id',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='cryptowithdraw',
            name='tx_id',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
