import datetime
import decimal
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db import models
from django.conf import settings
from django.utils import timezone
from .utils import get_users_match
User = get_user_model()


class MatchQuerySet(models.query.QuerySet):
    def all(self):
        return self.filter(active=True)

    def matches(self, user):
        q1 = self.filter(user_a=user).exclude(user_b=user)
        q2 = self.filter(user_b=user).exclude(user_a=user)
        return (q1 | q2).distinct()


class MatchManager(models.Manager):
    def get_queryset(self):

        return MatchQuerySet(self.model, using=self._db)

    def get_or_create_match(self, user_a=None, user_b=None):
        try:
            obj = self.get(user_a=user_a, user_b=user_b)
        except:
            obj = None
        try:
            obj_2 = self.get(user_a=user_b, user_b=user_a)
        except:
            obj_2 = None
        if obj and not obj_2:
            obj.check_update()
            return obj, False
        elif not obj and obj_2:
            obj_2.check_update()
            return obj_2, False
        else:
            new_instance = self.create(user_a=user_a, user_b=user_b)
            new_instance.do_match()
            return new_instance, True

    def update_all(self):
        queryset = self.all()
        now = timezone.now()
        offset = now - datetime.timedelta(seconds=12)
        offset2 = now - datetime.timedelta(hours=36)
        queryset.filter(updated__gt=offset2).filter(updated__lte=offset)
        if queryset.count > 0:
            for i in queryset:
                i.check_update()

    def matches_all(self, user):
        return self.get_queryset().matches(user)

    def get_matches(self, user):
        qs = self.get_queryset().matches(user)
        print('qs', qs)
        matches = []
        for match in qs:
            print(match.user_b)
            print(user)
            if match.user_a == user:
                print('match_user_a')
                match_to_list = [match.user_b]
                matches.append(match_to_list)
            elif match.user_b == user:
                print('match_user_b')
                match_to_list = [match.user_a]
                matches.append(match_to_list)
            else:
                pass
        print('matches', matches)
        return matches

    def get_percent_matches(self,user):
        qs = self.get_queryset().matches(user).order_by('-match_decimal')
        matches = []
        for match in qs:
            if match.user_a == user:
                match_to_list = [match.user_b, match.get_percent]
                matches.append(match_to_list)
            elif match.user_b == user:
                match_to_list = [match.user_a, match.get_percent]
                matches.append(match_to_list)
            else:
                pass
        return matches


class Match(models.Model):
    user_a = models.ForeignKey(User, on_delete=models.CASCADE, related_name='match_user_a')
    user_b = models.ForeignKey(User, on_delete=models.CASCADE, related_name='match_user_b')
    match_decimal = models.DecimalField(decimal_places=8, max_digits=16, default=0.00)
    questions_answered = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "%.2f" %(self.match_decimal)

    objects = MatchManager()

    @property
    def get_percent(self):
        new_decimal = self.match_decimal * Decimal(100)
        return "%.2f%%" % (new_decimal)

    def do_match(self):
        user_a = self.user_a
        user_b = self.user_b
        match_decimal, questions_answered = get_users_match(user_a, user_b)
        self.match_decimal = match_decimal
        self.questions_answered = questions_answered
        self.save()

    def check_update(self):
        now = timezone.now()
        offset = now - datetime.timedelta(seconds=12)  # 12 hours ago
        self.do_match()
        # else:
        #     print("already updated")





