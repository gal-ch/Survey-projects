# Generated by Django 3.0.5 on 2020-04-15 16:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_profile'),
        ('questions', '0006_auto_20200412_1850'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useranswer',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Profile'),
        ),
    ]