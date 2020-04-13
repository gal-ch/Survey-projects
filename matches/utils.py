from django.contrib.auth import get_user_model
from questions.models import UserAnswer
from decimal import Decimal
User = get_user_model()
users = User.objects.all()
all_user_answers = UserAnswer.objects.all().order_by("user__id")


def get_match(user_a, user_b):
    a_answers = UserAnswer.objects.filter(user=user_a)
    b_answers = UserAnswer.objects.filter(user=user_b)
    a_total_awarded = 0
    a_points_possible = 0
    num_question = 0
    for a in a_answers:
        for b in b_answers:
            if a.question_id == b.question_id:
                num_question += 1
                a_pref = a.other_user_answer
                b_answers = b.user_answer
                if a_pref == b_answers:
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
