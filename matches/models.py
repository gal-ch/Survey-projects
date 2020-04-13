import datetime

from django.db import models
from django.conf import settings
from django.utils import timezone

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
            obj_1.check_update()
            return obj_1, False
        elif obj_2 and not obj_1:
            obj_2.check_update()
            return obj_2, False
        else:
            new_instance = self.create(user_a=user_a, user_b=user_b)
            new_instance.do_match()
            return new_instance, True

    def update_all(self):
        queryset = self.all()
        now = timezone.now()
        offset1 = now - datetime.timedelta(hours=12)
        offset2 = now - datetime.timedelta(hours=36)
        queryset.filter(updated__gt=offset2).filter(updated__lte=offset1)
        if queryset.count > 0:
            for i in queryset:
                i.check_update()


class Match(models.Model):
    user_a = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='match_user_a')
    user_b = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='match_user_b')
    match_decimal = models.DecimalField(decimal_places=8, max_digits=16, default=0.00)
    questions_answered = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    objects = MatchManager()

    def do_match(self):
        user_a = self.user_a
        user_b = self.user_b
        match_decimal, questions_answered = get_users_match(user_a, user_b)
        self.match_decimal = match_decimal
        self.questions_answered = questions_answered
        self.save()

    def check_update(self):
        now = timezone.now()
        offset = now - datetime.timedelta(hours=12)
        if self.updated <= offset:
            self.do_match()
        else:
            print('already updated')





