from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, HTML, ButtonHolder, Submit
from .custom_layout_object import *
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import modelformset_factory
from django.forms.models import inlineformset_factory
from accounts.models import MyUser, Profile, UserJob
from datetimepicker.widgets import DateTimePicker


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = MyUser
        fields = (
            'username',
            'email',
            'password1',
            'password2'
        )


class ProfileForm(forms.ModelForm):
    # age = forms.DateTimeField(widget=DateTimePicker(),)
    class Meta:
        model = Profile
        fields = (
            'age',
            'bio',
            'gender',
            'picture',
                  )


class JobForm(forms.ModelForm):
    class Meta:
        model = UserJob
        fields = (
            'position',
            'location',
            'employer_name',
        )


JobFormset = modelformset_factory(UserJob, JobForm, can_delete=True, extra=3)




class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']

class JobForm(forms.ModelForm):
    class Meta:
        model = UserJob
        exclude = []
        # widgets = {
        #     'start': DateInput(attrs={'class':'datepicker'}),
        #     'end': DateInput(attrs={'class':'datepicker'}),
        # }


JobFormset = inlineformset_factory(Profile, UserJob, form=JobForm, extra=2)


