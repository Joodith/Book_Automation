from django.contrib import admin
from Account import models

# Register your models here.
admin.site.register(models.CustomUser)
admin.site.register(models.EmployeeID)
admin.site.register(models.ManagerID)
admin.site.register(models.Customer)
admin.site.register(models.Employee)
