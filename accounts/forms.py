

from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import MyUser, Profile


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = MyUser
        fields = ('username', 'email', 'password1', 'password2')


class ProfileForm(forms.ModelForm):
    # date_of_birth = forms.DateField(input_formats=['%d/%m/%Y %H:%M'])
    class Meta:
        model = Profile
        fields = ['age', 'bio', 'gender', 'picture']