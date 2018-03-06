# Generated by Django 2.0.2 on 2018-03-06 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exchange_core', '0023_auto_20180302_1716'),
    ]

    operations = [
        migrations.AddField(
            model_name='currencies',
            name='status',
            field=models.CharField(choices=[('active', 'active'), ('active', 'active'), ('inactive', 'inactive'), ('inactive', 'inactive')], default='active', max_length=30, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='users',
            name='status',
            field=models.CharField(choices=[('created', 'created'), ('approved_documentation', 'approved_documentation'), ('inactive', 'inactive'), ('disapproved_documentation', 'disapproved_documentation')], default='created', max_length=30, verbose_name='Status'),
        ),
    ]
