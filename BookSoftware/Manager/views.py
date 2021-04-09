from django.shortcuts import render
from django.views import generic
from django.http import JsonResponse
from django.urls import reverse_lazy,reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.core import serializers
from Customer.models import Bill,Suggestion
from Employee.models import BookCategory,Book
import json

# Create your views here.
class ManagerHomeView(generic.TemplateView):
    template_name="Manager/manager_home.html"

class BillView(generic.ListView):
    model=Bill
    context_object_name ="bills"
    template_name="Manager/bills_list.html"

class SalesStatisticsView(generic.TemplateView):
    template_name ="Manager/sales_statistics.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bk_categ=BookCategory.objects.all()
        category_list=[]
        for i in bk_categ:
            category_list.append(i.categ)
        categ_list=json.dumps(category_list)
        context['category_list']=categ_list
        chart=self.get_dict(category_list)
        chart_data=json.dumps(chart)
        context['chart_data']=chart_data
        print(chart)
        return context

    def get_dict(self,p):
        d={}
        chart=[]
        bill_products=[]
        all_bills=Bill.objects.all()
        for bill in all_bills:
            prod_list=bill.products_list.all()
            for prod in prod_list:
                bill_products.append(prod)
        for k in bill_products:
            for ctg in k.product.category.all():
                if ctg.categ in d:
                    d[ctg.categ]+=k.quantity
                else:
                    d[ctg.categ]=k.quantity


        for e in p:
            if e in d:
                chart.append(d[e])
            else:
                chart.append(0)
        return chart

class ManagerBookList(generic.ListView):
    model=Book
    context_object_name ="books_list"
    template_name="Manager/books_list.html"





    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        all_categ=BookCategory.objects.all()
        categ_list=[]
        for item in all_categ:
            categ_list.append(item.categ)
        context['categ_list']=categ_list
        li = serializers.serialize("json",Book.objects.all())
        context['json_li']=json.loads(li)
        context['ctg']=""
        context['length']=len(categ_list)
        return context





class UpdateBook(generic.UpdateView):
    model=Book
    fields="__all__"
    template_name="Employee/book_create.html"
    success_url =reverse_lazy("Manager:list_books")

class DeleteBook(generic.DeleteView):
    model=Book
    context_object_name ="bk"
    success_url = reverse_lazy("Manager:list_books")
    template_name ="Manager/confirm_delete.html"




class ViewCategoryWise(generic.ListView):
    model=Book
    template_name ="Manager/books_list.html"

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        ctg=self.kwargs.get('categ')
        bk_obj = Book.objects.all()
        bk_list = []
        pk_list = []
        for book in bk_obj:
            for a in book.category.all():
                if ctg == a.categ and book.pk not in pk_list:
                    pk_list.append(book.pk)
                    bk_list.append(book)
        li = serializers.serialize("json", bk_list)
        all_categ = BookCategory.objects.all()
        categ_list = []
        for item in all_categ:
            categ_list.append(item.categ)
        context['json_li']=json.loads(li)
        context['categ_list']=categ_list
        context['ctg']=ctg
        context['length']=len(bk_list)
        return context




class ViewSuggestions(generic.ListView):
    model=Suggestion
    ordering = ['-people_count']
    context_object_name ="sug_list"
    template_name="Manager/suggestions_view.html"

class ThresholdView(generic.ListView):
    model=Book
    template_name ="Manager/threshold.html"

    def get_queryset(self):
        self.books_list=Book.objects.all()

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        bk_li=[]
        for bk in self.books_list:
            q=bk.initial_copies
            value=(30*q)//100
            if bk.no_of_copies<=value:
                bk_li.append(bk)
        context['books_list']=bk_li
        context['length']=len(bk_li)
        return context






