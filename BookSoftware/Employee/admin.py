from django.contrib import admin
from Employee import models

# Register your models here.
admin.site.register(models.Book)
admin.site.register(models.BookCategory)

