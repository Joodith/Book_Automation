from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login,logout
from Account import models
from Account import forms
from Account.backends import EmailOrUsernameModelBackend

# Create your views here.
def CustomerRegisterView(request):
    if request.method=="POST":
        user_form=forms.UserRegisterForm(data=request.POST)
        cust_form=forms.CustomerRegisterForm(data=request.POST)
        if user_form.is_valid() and cust_form.is_valid():
            user=user_form.save(commit=False)
            user.status="Customer"
            if cust_form.cleaned_data['email']:
                mail=cust_form.cleaned_data['email']
                user.email=mail
            user.save()
            prof=cust_form.save(commit=False)
            prof.cust_user=user
            prof.save()
            return HttpResponseRedirect(reverse('Account:login'))
        else:
            messages.add_message(request,messages.ERROR,"Invalid form data")
            return render(request,"Account/CustomerRegister.html",{'user_form':user_form,'cust_form':cust_form})
    else:
        user_form=forms.UserRegisterForm()
        cust_form=forms.CustomerRegisterForm()
        return render(request,"Account/CustomerRegister.html",{'user_form':user_form,'cust_form':cust_form})


def ManagerRegisterView(request):
    if request.method=="POST":
        user_form=forms.UserRegisterForm(data=request.POST)
        manager_form=forms.EmployeeRegisterForm(data=request.POST)
        if user_form.is_valid() and manager_form.is_valid():
            user=user_form.save(commit=False)
            user.status="Manager"
            user.email=manager_form.cleaned_data['email']
            user.save()
            manager=manager_form.save(commit=False)
            try:
                check=models.ManagerID.objects.get(id_val=manager.employee_id);
            except check.DoesNotExist:
                messages.add_message(request,messages.ERROR,"Invalid Manager ID")
                return render(request,"Account/EmployeesRegister.html",{'user_form':user_form,'manager_form':manager_form})
            manager.emp_user=user
            manager.save()
            return HttpResponseRedirect(reverse('Account:login'))
        else:
            messages.add_message(request, messages.ERROR, "Invalid Manager ID")
            return render(request,"Account/EmployeesRegister.html",{'user_form':user_form,'manager_form':manager_form})
    else:
        user_form=forms.UserRegisterForm()
        manager_form=forms.EmployeeRegisterForm()
        return render(request,"Account/EmployeesRegister.html",{'user_form':user_form,'manager_form':manager_form})




def EmployeeRegisterView(request):
    if request.method=="POST":
        user_form=forms.UserRegisterForm(data=request.POST)
        employee_form=forms.EmployeeRegisterForm(data=request.POST)
        if user_form.is_valid() and employee_form.is_valid():
            user=user_form.save(commit=False)
            user.status="Employee"
            user.email=employee_form.cleaned_data['email']
            user.save()
            employee=employee_form.save(commit=False)
            try:
                check=models.EmployeeID.objects.get(id_val=employee.employee_id);
            except check.DoesNotExist:
                messages.add_message(request,messages.ERROR,"Invalid Employee ID")
                return render(request,"Account/EmployeesRegister.html",{'user_form':user_form,'manager_form':employee_form})
            employee.emp_user=user
            employee.save()
            return HttpResponseRedirect(reverse('Account:login'))
        else:
            messages.add_message(request, messages.ERROR, "Invalid Employee ID")
            return render(request,"Account/EmployeesRegister.html",{'user_form':user_form,'manager_form':employee_form})
    else:
        user_form=forms.UserRegisterForm()
        employee_form=forms.EmployeeRegisterForm()
        return render(request,"Account/EmployeesRegister.html",{'user_form':user_form,'manager_form':employee_form})

def LoginView(request):
    if request.method=="POST":
        login_form=forms.LoginForm(data=request.POST)
        username=request.POST.get('username')
        password=request.POST.get('password')
        if login_form.is_valid():
            auth_login=EmailOrUsernameModelBackend()
            user=auth_login.authenticate(username=username,password=password)
            if user:
                user.backend = 'Account.backends.EmailOrUsernameModelBackend'
                login(request,user)
                if user.status=="Employee":
                    return HttpResponseRedirect(reverse('Employee:emp_home'))
                elif user.status=="Customer":
                    return HttpResponseRedirect(reverse('Customer:customer_home'))
                else:
                    return HttpResponseRedirect(reverse('Manager:home_manager'))
            else:
                messages.add_message(request, messages.ERROR, 'Username or password is invalid')
                return render(request, "Account/login.html", {'login_form': login_form})

        else:
            messages.add_message(request,messages.ERROR,'Invalid form data')
            return render(request,"Account/login.html",{'login_form':login_form})
    else:
        login_form=forms.LoginForm()
        return render(request,"Account/login.html",{'login_form':login_form})

def ResetProcessStartView(request):
    if request.method=="POST":
        form=forms.ResetPasswordUserForm(data=request.POST)
        username=request.POST.get('username')
        if form.is_valid():
            auth_login = EmailOrUsernameModelBackend()
            user = auth_login.authenticate_only_username(username=username)
            if user:
                user.backend='Account.backends.EmailOrUsernameModelBackend'
                return HttpResponseRedirect(reverse('Account:password_reset',kwargs={'user':username}))
            else:
                messages.error(request,'User does not exist')
                return render(request, "Account/reset_start.html", {'form':form})
        else:
            messages.error(request, 'Invalid form data')
            return render(request, "Account/reset_start.html", {'form': form})
    else:
        form = forms.ResetPasswordUserForm()
        return render(request, "Account/reset_start.html", {'form': form})

def ResetPasswordView(request,user):
    if request.method=="POST":
        form=forms.ResetPasswordForm(data=request.POST)
        password=request.POST.get('password2')
        username = user
        auth_login = EmailOrUsernameModelBackend()
        user_auth = auth_login.authenticate_only_username(username=username)
        if form.is_valid():
            user_auth.set_password(password)
            user_auth.save()
            return HttpResponseRedirect(reverse('Account:login'))
        else:
            messages.error(request,"Passwords do not match")
            return render(request, "Account/reset_password.html", {'form': form})
    else:
        form = forms.ResetPasswordForm()
        return render(request, "Account/reset_password.html", {'form': form})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('Account:login'))







