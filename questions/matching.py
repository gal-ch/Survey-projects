from django.contrib.auth import get_user_model
from .models import UserAnswer
User = get_user_model()
users = User.objects.all()
all_user_answers = UserAnswer.objects.all().order_by("user__id")


def get_match(user_one, user_two):
    user_one_answers = UserAnswer.objects.filter(user=user_one)[0]
    user_two_answers = UserAnswer.objects.filter(user=user_two)[0]
    if user_one_answers.question.id == user_two_answers.question.id:
        user_one_answers = user_one_answers.user_answer
        user_one_pref = user_one_answers.other_user_answer
        user_two_answer = user_two_answers.user_answer
        user_two_pref = user_two_answers.other_user_answer
        if user_one_answers == user_two_pref:
            print("%s fits with %s's preference" % (user_one_answers.user.username, user_one_answers.user.username))
        if user_one_pref == user_two_answers:
            print("%s fits with %s's preference" % (user_two_answers.user.username, user_two_answers.user.username))
        if user_one_answers == user_two_pref and user_one_pref == user_two_answer:
            print("this is good answer for both")

