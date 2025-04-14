from django.db import models

class Expense(models.Model):
    category = models.CharField(max_length=50)
    amount = models.FloatField()
    date = models.DateField()
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.category} - ₹{self.amount} on {self.date}"
