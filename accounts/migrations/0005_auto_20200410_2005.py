# Generated by Django 3.0.5 on 2020-04-10 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20200410_1916'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='gender',
            field=models.IntegerField(choices=[(0, 'male'), (1, 'female'), (2, 'not specified')]),
        ),
    ]
