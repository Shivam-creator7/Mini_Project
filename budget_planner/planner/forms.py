from django import forms
from .models import Budget, Expense
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['Subject', 'Time']

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['Subject', 'Time', 'period']
        widgets = {
            'Subject': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'Time': forms.NumberInput(attrs={'class': 'form-control', 'required': True}),
            'period': forms.Select(attrs={'class': 'form-control', 'required': True}),
        }
