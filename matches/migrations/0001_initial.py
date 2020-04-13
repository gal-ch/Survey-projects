# Generated by Django 3.0.5 on 2020-04-13 13:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('match_decimal', models.DecimalField(decimal_places=8, default=0.0, max_digits=16)),
                ('questions_answered', models.IntegerField(default=0)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('user_a', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='match_user_a', to=settings.AUTH_USER_MODEL)),
                ('user_b', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='match_user_b', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]