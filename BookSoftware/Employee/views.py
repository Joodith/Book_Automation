from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from Employee import models
from Employee import forms
from Customer.models import Bill


# Create your views here.
class EmployeeHomeView(generic.TemplateView):
    template_name="Employee/emp_home.html"

class BookCreateView(generic.CreateView):
    form_class=forms.BookForm
    success_url=reverse_lazy('Employee:emp_home')
    template_name="Employee/book_create.html"

class BooksListView(generic.ListView):
    model=models.Book
    context_object_name ="books"
    template_name="Employee/all_books_list.html"

class BillView(generic.ListView):
    model=Bill
    context_object_name ="bills"
    template_name="Employee/bills_list.html"

