from django.db import models
from django.contrib.auth import get_user_model
from Employee.models import Book


User=get_user_model()

class UserProduct(models.Model):
    customer=models.ForeignKey(User,related_name="userproduct",on_delete=models.CASCADE)
    product=models.ForeignKey(Book,related_name="userproduct",on_delete=models.CASCADE)
    wishlist=models.BooleanField(default=False)
    cart=models.BooleanField(default=False)
    quantity=models.IntegerField(default=1)

class Address(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    pincode=models.IntegerField()
    addrs=models.CharField(max_length=100)
    locality=models.CharField(max_length=100)
    city=models.CharField(max_length=50)
    state=models.CharField(max_length=50)

class Bill(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    products_list=models.ManyToManyField(UserProduct)
    bill_amount=models.DecimalField(max_digits=10,decimal_places=2)
    date=models.DateTimeField()
    address=models.ForeignKey(Address,on_delete=models.CASCADE)

class Suggestion(models.Model):
    book=models.CharField(max_length=200)
    author_name=models.CharField(max_length=200,null=True,blank=True)
    people_count=models.IntegerField()

    def __str__(self):
        if self.book != "":
            return self.book
        elif self.author_name != "":
            return self.author_name




