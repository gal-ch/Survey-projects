from django import forms
LEVELS = (
    ('Mandatory', 'Mandatory'),
    ('Very important', 'Very important'),
    ('Somewhat important', 'Somewhat important'),
    ('Not important', 'Not important'),
)


class UserResponseForm(forms.Form):
    question_id = forms.IntegerField()
    answer_id = forms.IntegerField()
    importance_level = forms.ChoiceField(choices=LEVELS)


