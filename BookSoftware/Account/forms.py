from django import forms
from Account import models
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User=get_user_model()

class UserRegisterForm(UserCreationForm):
    class Meta:
        model=User
        fields=('username','password1','password2')
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text=None
        self.fields['username'].help_text = None


class CustomerRegisterForm(forms.ModelForm):
    error_messages={
        'exceed_length':'Phone number invalid',
        'email_exist':'Email already taken'
    }
    phone_no = forms.CharField(widget=forms.NumberInput(
        attrs={
            'style':'width:200px;height:40px',
            'id':'number',

        }
    ), required=True,help_text="10 digit mobile number",)
    email = forms.CharField(widget=forms.EmailInput(
        attrs={
            'style': 'width:200px;height:40px',

        }
    ), required=False,help_text="Not mandatory")
    class Meta:
        model=models.Customer
        fields=('fullname',)
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_email(self):
        if self.cleaned_data.get('email'):
            email=self.cleaned_data.get('email')
            qs=User.objects.filter(email=email)
            if qs.exists():
                raise forms.ValidationError(self.error_messages['email_exist'],code='email_exist')
            return email
    def clean_phone_no(self):
        ph_no=self.cleaned_data.get('phone_no')
        if len(str(ph_no))!=10:
            raise forms.ValidationError(self.error_messages['exceed_length'],code='exceed_length')
        return ph_no


    def save(self,commit=True):
        customer=super(CustomerRegisterForm,self).save(commit=False)
        customer.phone_no=self.cleaned_data['phone_no']
        if self.cleaned_data['email']:
            customer.email=self.cleaned_data['email']
        if commit:
            customer.save()
        return customer


class EmployeeRegisterForm(forms.ModelForm):
    error_messages = {
        'exceed_length': 'Phone number invalid',
        'email_exist': 'Email already taken'
    }
    phone_no = forms.CharField(widget=forms.NumberInput, required=True,help_text="10 digit mobile number")
    email = forms.CharField(widget=forms.EmailInput)
    class Meta:
        model=models.Employee
        fields=("employee_id","name","age")
    def clean_email(self):
        email=self.cleaned_data.get('email')
        qs=User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError(self.error_messages['email_exist'],code='email_exist')
        return email
    def clean_phone_no(self):
        ph_no=self.cleaned_data.get('phone_no')
        if len(str(ph_no))!=10:
            raise forms.ValidationError(self.error_messages['exceed_length'],code='exceed_length')
        return ph_no
    def save(self,commit=True):
        employee=super(EmployeeRegisterForm,self).save(commit=False)
        employee.phone_no=self.cleaned_data['phone_no']
        employee.email=self.cleaned_data['email']
        if commit:
            employee.save()
        return employee


class LoginForm(forms.Form):
    username=forms.CharField(required=True)
    password=forms.CharField(widget=forms.PasswordInput(),required=True)

class ResetPasswordUserForm(forms.Form):
    error_messages={
        'mismatch':'Passwords do not match'
    }
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'style':'height:39px;width:300px',
            'placeholder':'Username/email'
        }
    ),required=True,error_messages={'invalid':"Invalid username or email"})

class ResetPasswordForm(forms.Form):
    error_messages = {
        'mismatch': 'Passwords do not match'
    }
    password1= forms.CharField(widget=forms.PasswordInput(
        attrs={
            'style': 'height:39px;width:300px',
            'placeholder': 'Password'
        }
    ), required=True)
    password2= forms.CharField(widget=forms.PasswordInput(
        attrs={
            'style': 'height:39px;width:300px',
            'placeholder':'Confirm Password'
        }
    ), required=True)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(self.error_messages['mismatch'],code='mismatch')
        return password2






