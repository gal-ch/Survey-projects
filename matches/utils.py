from django.contrib.auth import get_user_model
from questions.models import UserAnswer
from decimal import Decimal
User = get_user_model()
users = User.objects.all()
all_user_answers = UserAnswer.objects.all().order_by("user__id")


def get_points(user_a, user_b):
    a_answers = UserAnswer.objects.filter(user=user_a)
    b_answers = UserAnswer.objects.filter(user=user_b)
    a_total_awarded = 0
    a_points_possible = 0
    num_question = 0
    for a in a_answers:
        print('a:', a)
        print('b_answers:', b_answers)
        for b in b_answers:
            print('b:', b)
            if a.question.id == b.question.id:
                num_question += 1
                a_pref = a.other_user_answer
                b_answer = b.user_answer
                if a_pref == b_answer:
                    '''
                    a give point to b according to the importance level of a
                    '''
                    a_total_awarded += a.other_user_points
                '''
                assign total points
                '''
                a_points_possible += a.other_user_points
            print('{} give {} point of {} to {} '.format(user_a, a_total_awarded, a_points_possible, user_b))
    percent = a_total_awarded / Decimal(a_points_possible)
    print(percent, num_question)
    if percent == 0:
        percent = 0.000001
    return percent, num_question


def get_users_match(user_a, user_b):
    a = get_points(user_a, user_b)
    b = get_points(user_b, user_a)
    number_of_question = b[1]
    match_decimal = (Decimal(a[0] * Decimal(b[0])) ** (1/Decimal(b[1])))
    return match_decimal, number_of_question
