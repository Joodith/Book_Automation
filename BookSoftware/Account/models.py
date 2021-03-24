from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.
class CustomUser(AbstractUser):
    status=models.CharField(max_length=30)

class EmployeeID(models.Model):
    id_val=models.CharField(max_length=10)
    def __str__(self):
        return self.id_val

class ManagerID(models.Model):
    id_val=models.CharField(max_length=10)

    def __str__(self):
        return self.id_val

class Employee(models.Model):
    emp_user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    employee_id=models.CharField(max_length=10,unique=True)
    name=models.CharField(max_length=50)
    age=models.IntegerField()
    phone_no=models.BigIntegerField()

    def __str__(self):
        return self.emp_user.username

class Customer(models.Model):
    cust_user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    fullname=models.CharField(max_length=50)
    phone_no = models.BigIntegerField()

    def __str__(self):
        return self.cust_user.username






