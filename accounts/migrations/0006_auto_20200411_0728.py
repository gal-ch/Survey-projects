# Generated by Django 3.0.5 on 2020-04-11 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20200410_2005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='gender',
            field=models.IntegerField(choices=[(0, 'male'), (1, 'female'), (2, 'not specified')], default=2),
        ),
    ]