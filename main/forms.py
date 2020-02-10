from django import forms
from django.contrib.auth.models import User


class ChangeUserInfoForm(forms.ModelForm):
    email = forms.EmailField(required=True,
                             label='Адрес электронной почты')

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
