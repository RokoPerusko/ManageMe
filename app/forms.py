from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Obavezno. Unesite ispravnu email adresu.')
    first_name = forms.CharField(max_length=30, required=False, help_text='Opcionalno.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Opcionalno.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'date', 'time', 'color', 'description', 'completed']

        widgets = {
            'date': forms.DateInput(format='%d.%m.%Y.', attrs={'type': 'date'}),
            'time': forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
            'completed': forms.CheckboxInput(),
        }


class DiaryEntryForm(forms.ModelForm):
    class Meta:
        model = DiaryEntry
        fields = ['title', 'description']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio']




