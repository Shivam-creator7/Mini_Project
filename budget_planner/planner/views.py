from django.shortcuts import render, redirect
from .forms import BudgetForm, ExpenseForm, RegisterForm
from .models import Budget, Expense
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from decimal import Decimal

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'planner/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'planner/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

from decimal import Decimal
from django.db.models import Sum


@login_required
def dashboard(request):
    budgets = Budget.objects.filter(user=request.user)
    expenses = Expense.objects.filter(user=request.user)
    alerts = []

    for budget in budgets:
        total = expenses.filter(Subject=budget.Subject).aggregate(Sum('Time'))['Time__sum'] or 0
        
        if total >= budget.Time:
            alerts.append(f"Very Good: {budget.Subject} hours exceeded! Total time spent: {total} out of {budget.Time}.")
        elif total >= Decimal("0.9") * budget.Time:
            alerts.append(f"Good: Almost near your required {budget.Subject} study hours! Total time spent: {total} out of {budget.Time}.")
        elif total < Decimal("0.9") * budget.Time:
            alerts.append(f"Do: Study {budget.Subject} to complete your daily goals. Total time spent: {total} out of {budget.Time}.")

    if not budgets.exists():
        alerts.append("Start by adding your study goals.")

    return render(request, 'planner/dashboard.html', {
        'budgets': budgets,
        'expenses': expenses,
        'alerts': alerts
    })



@login_required
def add_budget(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            budget.save()
            return redirect('dashboard')
    else:
        form = BudgetForm()
    return render(request, 'planner/add_budget.html', {'form': form})


@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            return redirect('dashboard')
    else:
        form = ExpenseForm()
    return render(request, 'planner/form.html', {'form': form, 'title': 'Add Expense'})

@login_required
def home(request):
    budgets = Budget.objects.filter(user=request.user)
    expenses = Expense.objects.filter(user=request.user)
    return render(request, 'planner/home.html', {'budgets': budgets, 'expenses': expenses})