from django.conf.urls import url
from Account import views
app_name='Account'

urlpatterns=[
    url(r'^customer_register/$',views.CustomerRegisterView,name="customer_register"),
    url(r'^manager_register/$',views.ManagerRegisterView,name="manager_register"),
    url(r'^employee_register/$',views.EmployeeRegisterView,name="employee_register"),
    url(r'^login/$',views.LoginView,name="login"),
    url(r'^reset_start/$',views.ResetProcessStartView,name="start_reset"),
    url(r'^reset_password/(?P<user>[-\w]+)/$',views.ResetPasswordView,name="password_reset"),
    url(r'^logout/$',views.user_logout,name="logout"),

]