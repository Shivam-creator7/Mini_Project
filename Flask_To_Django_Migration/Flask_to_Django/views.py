from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Expense
from datetime import datetime
from django.db.models import Sum
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .configure import CATEGORIES  # ✅ Import your categories from configure.py

# Just a dummy user ID (since no auth system)
DUMMY_USER_ID = 1

def home(request):
    return render(request, "home.html")


def dashboard(request):
    search_term = request.GET.get("search", "")
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    expenses = Expense.objects.all()

    if search_term:
        expenses = expenses.filter(category__icontains=search_term) | expenses.filter(description__icontains=search_term)

    if start_date:
        expenses = expenses.filter(date__gte=start_date)
    if end_date:
        expenses = expenses.filter(date__lte=end_date)

    expenses = expenses.order_by('-date')
    total_expense = expenses.aggregate(Sum('amount'))['amount__sum'] or 0

    category_totals = {}
    for expense in expenses:
        category_totals[expense.category] = category_totals.get(expense.category, 0) + expense.amount

    top_category = max(category_totals, key=category_totals.get, default="N/A")
    expense_labels = list(category_totals.keys())
    expense_values = list(category_totals.values())

    expense_trends = {}
    for expense in expenses:
        date_str = expense.date.strftime("%Y-%m-%d")
        expense_trends[date_str] = expense_trends.get(date_str, 0) + expense.amount

    context = {
        "expenses": expenses,
        "total_expense": total_expense,
        "top_category": top_category,
        "expense_labels": expense_labels,
        "expense_values": expense_values,
        "expense_dates": list(expense_trends.keys()),
        "expense_amounts": list(expense_trends.values()),
        "search_term": search_term,
        "start_date": start_date,
        "end_date": end_date,
        "CATEGORIES": CATEGORIES  # ✅ Pass categories to template
    }

    return render(request, "dashboard.html", context)


def add_expense(request):
    if request.method == "POST":
        category = request.POST.get("category")
        amount = float(request.POST.get("amount"))
        date = datetime.strptime(request.POST.get("date"), "%Y-%m-%d")
        description = request.POST.get("description")

        Expense.objects.create(
            
            category=category,
            amount=amount,
            date=date,
            description=description
        )
        messages.success(request, "Expense added successfully!")
        return redirect("dashboard")

    return render(request, "add_expense.html", {"CATEGORIES": CATEGORIES})  # ✅


def edit_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)

    if request.method == "POST":
        expense.category = request.POST.get("category")
        expense.amount = float(request.POST.get("amount"))
        expense.date = datetime.strptime(request.POST.get("date"), "%Y-%m-%d")
        expense.description = request.POST.get("description")
        expense.save()
        messages.success(request, "Expense updated successfully!")
        return redirect("dashboard")

    return render(request, "edit_expense.html", {
        "expense": expense,
        "CATEGORIES": CATEGORIES
    })


    return render(request, "edit_expense.html", {
        "expense": expense,
        "CATEGORIES": CATEGORIES  # ✅
    })


def delete_expense(request, expense_id):
    if request.method == "POST":
        try:
            expense = Expense.objects.get(id=expense_id)
            expense.delete()
            return JsonResponse({"success": True})
        except Expense.DoesNotExist:
            return JsonResponse({"error": "Expense not found"}, status=404)
    return JsonResponse({"error": "Invalid request"}, status=400)