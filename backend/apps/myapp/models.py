from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    
    def __str__(self):
        return self.name
    
class React(models.Model):
    employee = models.CharField(max_length=30)
    department = models.CharField(max_length=200)



class SalesData(models.Model):
    month = models.CharField(max_length=20)
    sales = models.IntegerField()

    def __str__(self):
        return f"{self.month}: ${self.sales}"
    
