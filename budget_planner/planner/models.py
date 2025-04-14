from django.db import models
from django.contrib.auth.models import User

class Budget(models.Model):
    CATEGORY_CHOICES = [
        ('Maths','Maths'),
        ('Physics','Physics'),
        ('Chemistry','Chemistry'),
        ('Computer','Computer')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Subject = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    Time = models.DecimalField(max_digits=10, decimal_places=2)
    period = models.CharField(max_length=10, choices=[('Monthly', 'Monthly'), ('Daily', 'Daily')])

    def __str__(self):
        return f'{self.user.username} - {self.Subject} - {self.Time}'

class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('Maths', 'Maths'),
        ('Physics', 'Physics'),
        ('Chemistry', 'Chemistry'),
        ('Computer', 'Computer')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Subject = models.CharField(max_length=20, choices=CATEGORY_CHOICES)  # Correct field name
    Time = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.Subject} - {self.Time}'
