from django.conf.urls import url
from Employee import views
app_name="Employee"

urlpatterns=[
    url(r'^$',views.EmployeeHomeView.as_view(),name="emp_home"),
    url(r'^create_book/$',views.BookCreateView.as_view(),name="create_book"),
    url(r'^list_books/$',views.BooksListView.as_view(),name="list_book"),
    url(r'^bill_view/$',views.BillView.as_view(),name="manage_bill"),
]