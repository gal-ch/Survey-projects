from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save, pre_save
from accounts.models import MyUser, Profile

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
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user_answer = models.ForeignKey(Answer, related_name='user_answer', on_delete=models.CASCADE)
    user_importance_level = models.CharField(max_length=50, choices=LEVELS)
    user_answer_points = models.IntegerField(default=-1)
    other_user_answer = models.ForeignKey(Answer, null=True, blank=True, related_name='match_answer', on_delete=models.CASCADE)
    other_user_importance_level = models.CharField(max_length=50, choices=LEVELS)
    other_user_points = models.IntegerField(default=-1)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)


def score_importance(importance_level):
    if importance_level == 'Mandatory':
        points = 300
    elif importance_level == 'Very important':
        points = 200
    elif importance_level == 'Somewhat important':
        points = 50
    elif importance_level == 'Not important':
        points = 0
    else:
        points = 0
    return points


def update_user_answer_score(sender, instance, *args, **kwargs):
    user_point = score_importance(instance.user_importance_level)
    instance.user_answer_points = user_point
    other_user_point = score_importance(instance.other_user_importance_level)
    instance.other_user_points = other_user_point


pre_save.connect(update_user_answer_score, sender=UserAnswer)

