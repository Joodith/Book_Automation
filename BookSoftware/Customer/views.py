from django.shortcuts import render
from django.views import generic
from django.contrib import messages
from django.http import HttpResponseRedirect,HttpResponse,JsonResponse
from django.urls import reverse
from django.template.loader import get_template
from Customer import forms
from django.core.mail import send_mail,EmailMultiAlternatives
from django.contrib.auth import settings
from django.contrib.auth import get_user_model
from Employee.models import Book
from Customer.models import UserProduct,Address,Bill,Suggestion
import datetime

User=get_user_model()
# Create your views here.
class CustomerHomeView(generic.TemplateView):
    template_name="Customer/customer_home.html"

    def post(self,request,*args,**kwargs):
        search_param = request.POST.get('query')
        return HttpResponseRedirect(reverse('Customer:search_book',kwargs={'query':search_param}))

    def get(self, request, *args, **kwargs):
        return render(request,"Customer/customer_home.html",{'cur_user':request.user})




def BookSearchView(request,query):
    try:
        search_list_by_title = Book.objects.filter(title__icontains=query)
        search_list_by_author = Book.objects.filter(author__icontains=query)
    except:
        return HttpResponse("No such author or book!!")

    total_list = []
    if len(search_list_by_title) != 0:
        total_list += search_list_by_title
    if len(search_list_by_author) != 0:
        total_list += search_list_by_author
    context={}
    temp=request.user.userproduct.all()
    user_product_list=[]
    wish_list=[]
    cart_list=[]
    for k in temp:
        if k.wishlist:
            wish_list.append(k.product.pk)
        if k.cart:
            cart_list.append(k.product.pk)
        user_product_list.append(k.product.pk)
    context['prod_list']=user_product_list
    context['wish_list']=wish_list
    context['cart_list']=cart_list
    return render(request,"Customer/search_query.html",{'list':total_list,'cur_user':request.user,'context':context})

class BookDetailView(generic.DetailView):
    model=Book
    template_name="Customer/detail_book.html"

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['cur_user']=self.request.user
        req_book=Book.objects.get(pk=self.kwargs.get('pk'))
        temp = self.request.user.userproduct.all()
        context['wish_list'] =False
        context['cart_list'] =False
        for k in temp:
            if k.product.pk==req_book.pk:
                if k.wishlist:
                    context['wish_list']=True
                if k.cart:
                    context['prod_list']=True


        return context

def AddWishlistView(request):
    pk=request.GET['pk']
    book=Book.objects.get(pk=pk)
    user=request.user
    data={}
    prod_exist=False
    try:
        prod=UserProduct.objects.get(customer=user,product=book)
        prod_exist=True
    except:
        user_prod=UserProduct.objects.create(customer=user,product=book)
    if not prod_exist:
        user_prod.wishlist=True
        user_prod.save()
    data['prod_exist']=prod_exist
    return JsonResponse(data)

class WishlistView(generic.ListView):
    model=UserProduct
    template_name="Customer/wishlist.html"

    def get_queryset(self):
        cur_user = User.objects.get(username=self.kwargs.get('user'))
        self.temp = cur_user.userproduct.filter(wishlist=True)

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs);
        context['wishlist']=self.temp
        context['length']=len(self.temp)
        context['cur_user']=User.objects.get(username=self.kwargs.get('user'))
        return context

def DeleteWishList(request):
    pk=request.GET['pk']
    job=request.GET['job']
    book=Book.objects.get(pk=pk)
    user_prod=UserProduct.objects.get(customer=request.user,product=book)
    if job=="move_cart":
        user_prod.wishlist=False
        user_prod.cart=True
        user_prod.save()
    elif job=="remove":
        user_prod.delete()

    data={'message':"Book added to cart"}
    return JsonResponse(data)

def ChangeCart(request):
    pk = request.GET['pk']
    job = request.GET['job']
    book = Book.objects.get(pk=pk)
    user_prod = UserProduct.objects.get(customer=request.user, product=book)
    if job == "move_wishlist":
        user_prod.wishlist =True
        user_prod.cart = False
        user_prod.save()
    elif job == "remove":
        user_prod.delete()

    data = {'message': "Book added to wishlist!"}
    return JsonResponse(data)

class CartView(generic.ListView):
    model=UserProduct
    template_name = "Customer/cart.html"

    def get_queryset(self):
        self.sum_of_prices=0;
        cur_user = User.objects.get(username=self.kwargs.get('user'))
        self.temp = cur_user.userproduct.filter(wishlist=False,cart=True)
        for item in self.temp:
            self.sum_of_prices+=item.product.price*item.quantity;

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs);
        context['cartlist'] = self.temp
        context['cur_user'] = User.objects.get(username=self.kwargs.get('user'))
        context['numbers']=range(1,10);
        context['sum_of_prices']=self.sum_of_prices
        context['length'] = len(self.temp)
        return context
def ChangeQuantityView(request):
    pk=request.GET['pk']
    no=request.GET['no']
    book = Book.objects.get(pk=pk)
    user_prod = UserProduct.objects.get(customer=request.user, product=book)
    user_prod.quantity=int(no)
    user_prod.save()
    amt=book.price*int(no)
    data={'amount': amt}
    return JsonResponse(data)

def AddAddressView(request):
    if request.method=="POST":
        name=request.POST['name']
        phone_no = request.POST['phone_no']
        email=request.POST['email']
        pincode = request.POST['pincode']
        addrs= request.POST['addrs']
        locality= request.POST['locality']
        city = request.POST['city']
        state= request.POST['state']
        addr=Address.objects.create(user=request.user,pincode=pincode,addrs=addrs,locality=locality,city=city,state=state)
        final_prod=request.user.userproduct.filter(cart=True)
        total_price=0
        for i in final_prod:
            bk=Book.objects.get(pk=i.product.pk)
            bk.no_of_copies-=i.quantity
            bk.save()
            total_price+=i.product.price*i.quantity
        context={'final_prod':final_prod,'total_price':total_price}
        recipient=email
        subject="Greetings from Book Cafe!"
        with open(settings.BASE_DIR+"/Customer/templates/Customer/invoice.txt") as fl:
            tell_message=fl.read()
        message=EmailMultiAlternatives(subject=subject,
                  body=tell_message, from_email=settings.EMAIL_HOST_USER, to=[recipient])
        html_template=get_template("Customer/invoice.html").render(context=context)
        message.attach_alternative(html_template,"text/html")
        message.send()
        bill_obj=Bill(user=request.user,address=addr,bill_amount=total_price,date=datetime.datetime.now())
        bill_obj.save()
        bill_obj.products_list.set(final_prod)
        for prod in final_prod:
            prod.cart=False
            prod.save()
        #send_mail(subject,
                  #message, settings.EMAIL_HOST_USER, [recipient], fail_silently=False)
        return HttpResponseRedirect(reverse("Customer:order_success"))

    else:
        return render(request,"Customer/address.html",{'cur_user':request.user})


def SuccessOrderView(request):
    return render(request,"Customer/order_placed.html")

def TransactionView(request):
    try:
        all_bills=Bill.objects.filter(user=request.user)
    except:
        all_bills=[]
    return render(request,"Customer/transactions.html",{'all_bills':all_bills,'cur_user':request.user})


def SuggestView(request):
    if request.method=="POST":
        bk_name = request.POST.get('book_name')
        author = request.POST.get('author')
        print(bk_name)
        print(author)
        if bk_name == "" and author == "":
            messages.error(request, "Enter book title or author name!")
            return render(request, "Customer/suggestions.html", {'cur_user': request.user})
        try:
            exist_books = Book.objects.filter(title__icontains=bk_name)
        except:
            exist_books = []
        if len(exist_books) == 0:
            exist_suggestion = Suggestion.objects.filter(book__icontains=bk_name)
            if len(exist_suggestion)==0:
                exist_suggestion_ex = Suggestion(book=bk_name)
                if author != "":
                    exist_suggestion_ex.author_name = author
                    exist_suggestion_ex.people_count = 0
                    exist_suggestion_ex.save()
            else:
                for i in exist_suggestion:
                    i.people_count+=1
                    i.save()





        else:
            return HttpResponseRedirect(reverse('Customer:search_book', kwargs={'query': bk_name}))

        return HttpResponseRedirect(reverse("Customer:suggest_success"))

    return render(request,"Customer/suggestions.html",{'cur_user':request.user,'message':0})

def SuccessSuggest(request):
    return render(request, "Customer/success_suggestion.html", {'cur_user': request.user})



















