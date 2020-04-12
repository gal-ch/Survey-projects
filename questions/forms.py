from django import forms
from questions.models import LEVELS, Answer, Question


class UserResponseForm(forms.Form):
    question_id = forms.IntegerField()
    answer_id = forms.IntegerField()
    user_importance_level = forms.ChoiceField(choices=LEVELS)
    other_user_answer_id = forms.IntegerField()
    other_user_importance_level = forms.ChoiceField(choices=LEVELS)

    def clean_question_id(self):
        question_id = self.cleaned_data.get('question_id')
        print('question_id-form', question_id)
        try:
            obj = Question.objects.get(id=question_id)
        except:
            raise forms.ValidationError('It Same to have some problem with your question, please try again, thanks')
        return question_id

    def clean_answer_id(self):
        answer_id = self.cleaned_data.get('answer_id')
        try:
            obj = Answer.objects.get(id=answer_id)
        except:
            raise forms.ValidationError('It Same to have some problem with your answer, please try again, thanks')
        return answer_id

    def clean_other_user_answer_id(self):
        other_user_answer_id = self.cleaned_data.get('other_user_answer_id')
        try:
            obj = Answer.objects.get(id=other_user_answer_id)
        except:
            raise forms.ValidationError('It Same to have some problem with the other user answer, please try again, thanks')
        return other_user_answer_id









