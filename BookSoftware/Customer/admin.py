from django.contrib import admin
from Customer.models import UserProduct,Address,Bill,Suggestion
# Register your models here.
admin.site.register(UserProduct)
admin.site.register(Address)
admin.site.register(Bill)
admin.site.register(Suggestion)
