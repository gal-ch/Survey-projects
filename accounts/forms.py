
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import modelformset_factory

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
