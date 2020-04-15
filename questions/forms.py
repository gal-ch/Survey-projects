from django import forms
from django.forms import ModelForm
from questions.models import LEVELS, Answer, Question, UserAnswer


class UserResponseForm(ModelForm):
    user_importance_level = forms.ChoiceField(choices=LEVELS)
    other_user_importance_level = forms.ChoiceField(choices=LEVELS)
    user_answer = forms.ModelChoiceField(
        required=True,
        widget=forms.RadioSelect(),
        queryset=None,
        initial=None,
    )

    other_user_answer = forms.ModelChoiceField(
        required=True,
        widget=forms.RadioSelect(),
        queryset=None,
        initial=None,
    )

    class Meta:
        model = UserAnswer
        fields = ('user_answer', 'user_importance_level',
                  'other_user_answer','other_user_importance_level')

    def __init__(self, initial=None, *args, **kwargs,):
        super(UserResponseForm, self).__init__(*args, **kwargs)
        data = initial['data']
        print(data.user_answer)
        if initial:
            self.fields['user_answer'].queryset = Answer.objects.filter(question_id=initial['pk'])
            self.fields['user_answer'].initial = data.user_answer
            self.fields['other_user_answer'].queryset = Answer.objects.filter(question_id=initial['pk'])
            self.fields['other_user_answer'].initial = data.other_user_answer














