"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms import ModelForm
from .models import Task
from django.utils.translation import gettext_lazy as _


class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder': 'Password'}))


class DateInput(forms.DateInput):
    input_type = 'date'


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'complete', 'priority', 'due_date', 'status']
        widgets = {
            'due_date': DateInput(),
        }