from django.contrib.auth import get_user_model
from django.db.models import Q
from questions.models import UserAnswer, Question
from decimal import Decimal
User = get_user_model()
users = User.objects.all()
all_user_answers = UserAnswer.objects.all().order_by("user__id")


def get_users_match(user_a, user_b):
    q1 = Q(useranswer__user=user_a)
    q2 = Q(useranswer__user=user_b)
    question_set = Question.objects.filter(q1 | q2).distinct()
    a_points = 0
    b_points = 0
    a_total_point = 0
    b_total_point = 0
    question_in_common = 0
    for question in question_set:
        try:
            a = UserAnswer.objects.get(user=user_a, question=question)
        except:
            a = None
        try:
            b = UserAnswer.objects.get(user=user_b, question=question)
        except:
            b = None
        if a and b:
            question_in_common += 1
            if a.other_user_answer == b.user_answer:
                b_points += a.other_user_points
            b_total_point += a.other_user_points

            if b.other_user_answer == a.user_answer:
                a_points += b.other_user_points
            a_total_point += b.other_user_points
        if question_in_common > 0:
            a_decimal = a_points / Decimal(a_total_point)
            b_decimal = b_points / Decimal(b_total_point)
            print(a_decimal, b_decimal)
            if a_decimal == 0:
                a_decimal = 0.000001
            if b_decimal == 0:
                b_decimal = 0.000001
            match_percentage = (Decimal(a_decimal) * Decimal(b_decimal)) ** (1/Decimal(question_in_common))
            return match_percentage, question_in_common
        else:
            return 0.0, 0


