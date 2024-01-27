from django.contrib.auth.models import User
from django import forms
from .models import Profile

class UserEdit(forms.ModelForm):
        class Meta:
                model = User
                fields = ['username','first_name']

class ProfileEdit(forms.ModelForm):
        class Meta:
                model = Profile
                fields = ['date_of_bithd']

class LoginForm(forms.Form):
        username = forms.CharField(max_length=100)
        password = forms.CharField(widget=forms.PasswordInput)

class UserForm(forms.ModelForm):
        class Meta:
                model = User
                fields = ['username','first_name','email']
        password = forms.CharField(max_length=100, label='password',widget = forms.PasswordInput)
        password2 = forms.CharField(max_length=100, label = 'repeat_password',widget=forms.PasswordInput)

        def clean_password2(self):
                cd =self.cleaned_data
                if cd['password'] != cd['password2']:
                        raise forms.ValidationError('Valid_error')
                return cd['password2']

