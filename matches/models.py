from django.db import models
from django.conf import settings
from .utils import get_users_match


class MatchManager(models.Manager):
    def get_or_create_match(self, user_a=None, user_b=None):
        try:
            obj_1 = self.get(user_a=user_a, user_b=user_b)
        except:
            obj_1 = None
        try:
            obj_2 = self.get(user_a=user_b, user_b=user_a)
        except:
            obj_2 = None
        if obj_1 and not obj_2:
            return obj_1, False
        elif obj_2 and not obj_1:
            return obj_2, False
        else:
            new_instance = self.create(user_a=user_a, user_b=user_b)
            match_decimal, questions_answered = get_users_match(user_a, user_b)
            new_instance.match_decimal = match_decimal
            new_instance.questions_answered = questions_answered
            new_instance.save()
            return new_instance, True

            # need to: add match && save new_instance && return new_instance, True


class Match(models.Model):
    user_a = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='match_user_a')
    user_b = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='match_user_b')
    match_decimal = models.DecimalField(decimal_places=8, max_digits=16, default=0.00)
    questions_answered = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    objects = MatchManager()


