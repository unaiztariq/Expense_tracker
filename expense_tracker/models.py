from django.db import models

# Create your models here.

class Expense(models.Model):
    user_id = models.IntegerField()
    date = models.DateTimeField()
    exp_category = models.CharField(max_length=200)
    exp_amount = models.BigIntegerField()

    