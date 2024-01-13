from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# class SignupForm(UserCreationForm):
#      class Meta:
#          model = User
#          fields = ['username', 'password1', 'password2']
         

class RegisterUserForm(UserCreationForm):
    email = forms.EmailField()
    username = forms.CharField(max_length=50)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
   

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)