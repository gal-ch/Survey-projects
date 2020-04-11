from django.contrib.auth import get_user_model
from django.db import models

from accounts.models import MyUser

User = get_user_model()

class Question(models.Model):
    text = models.TextField()
    active = models.BooleanField(default=True)
    draft = models.BooleanField(default=False)
    timestemp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.text[:10]


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=120)
    active = models.BooleanField(default=True)
    draft = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.text[:10]

LEVELS = (
    ('Mandatory', 'Mandatory'),
    ('Very important', 'Very important'),
    ('Somewhat important', 'Somewhat important'),
    ('Not important', 'Not important'),
)


class UserAnswer(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    my_answer = models.ForeignKey(Answer, related_name='user_answer', on_delete=models.CASCADE)
    my_answer_importance = models.CharField(max_length=50, choices=LEVELS)
    other_user_answer = models.ForeignKey(Answer, null=True, blank=True, related_name='match_answer', on_delete=models.CASCADE)
    other_user_importance = models.CharField(max_length=50, choices=LEVELS)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

