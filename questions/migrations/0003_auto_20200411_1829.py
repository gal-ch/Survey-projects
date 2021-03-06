# Generated by Django 3.0.5 on 2020-04-11 18:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('questions', '0002_answer'),
    ]

    operations = [
        migrations.RenameField(
            model_name='answer',
            old_name='timestemp',
            new_name='timestamp',
        ),
        migrations.CreateModel(
            name='UserAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('my_answer_importance', models.CharField(choices=[('Mandatory', 'Mandatory'), ('Very important', 'Very important'), ('Somewhat important', 'Somewhat important'), ('Not important', 'Not important')], max_length=50)),
                ('other_user_importance', models.CharField(choices=[('Mandatory', 'Mandatory'), ('Very important', 'Very important'), ('Somewhat important', 'Somewhat important'), ('Not important', 'Not important')], max_length=50)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('my_answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_answer', to='questions.Answer')),
                ('other_user_answer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='match_answer', to='questions.Answer')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questions.Question')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
