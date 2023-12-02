from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm

from .models import User, Question


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control bg-dark border-primary text-white'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control bg-dark border-primary text-white'}))


class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control bg-dark border-primary text-white'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control bg-dark border-primary text-white'}),
        }


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control bg-dark border-primary text-white'}))
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control bg-dark border-primary text-white'}))
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control bg-dark border-primary text-white'}))


class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control bg-dark border-primary text-white'}),
            'email': forms.EmailInput(attrs={'class': 'form-control bg-dark border-primary text-white'}),
        }


class NewQuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['image', 'right_answer', 'wrong_answer_1', 'wrong_answer_2', 'wrong_answer_3', 'wrong_answer_4']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control bg-dark border-primary text-white'}),
            'right_answer': forms.TextInput(attrs={'class': 'form-control bg-dark border-primary text-white'}),
            'wrong_answer_1': forms.TextInput(attrs={'class': 'form-control bg-dark border-primary text-white'}),
            'wrong_answer_2': forms.TextInput(attrs={'class': 'form-control bg-dark border-primary text-white'}),
            'wrong_answer_3': forms.TextInput(attrs={'class': 'form-control bg-dark border-primary text-white'}),
            'wrong_answer_4': forms.TextInput(attrs={'class': 'form-control bg-dark border-primary text-white'}),
        }
