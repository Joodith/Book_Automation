from django.db import models
from django.contrib.auth import get_user_model


User=get_user_model()

# Create your models here.
class BookCategory(models.Model):
    categ=models.CharField(max_length=100)
    def __str__(self):
        return self.categ




class Book(models.Model):
    title=models.CharField(max_length=100)
    isbn=models.CharField(max_length=13,unique=True)
    author=models.CharField(max_length=50)
    year=models.DateField()
    publications=models.CharField(max_length=200)
    edition=models.IntegerField()
    price=models.DecimalField(max_digits=6,decimal_places=2)
    category=models.ManyToManyField(BookCategory)
    book_pic=models.ImageField(upload_to="book_pictures/")
    no_of_copies=models.IntegerField()
    initial_copies=models.IntegerField()

    def __str__(self):
        return self.title



