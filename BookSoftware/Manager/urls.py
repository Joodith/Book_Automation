from django.conf.urls import url
from Manager import views
app_name="Manager"

urlpatterns=[
    url(r'^home/$',views.ManagerHomeView.as_view(),name="home_manager"),
    url(r'^bills_list/$',views.BillView.as_view(),name="bill_view"),
    url(r'^sales/$',views.SalesStatisticsView.as_view(),name="statistics"),
    url(r'^books_list/$',views.ManagerBookList.as_view(),name="list_books"),
    url(r'^update_book/(?P<pk>\d+)/$',views.UpdateBook.as_view(),name="update_book"),
    url(r'^delete_book/(?P<pk>\d+)/$',views.DeleteBook.as_view(),name="delete_book"),
    url(r'^view_suggestions/$',views.ViewSuggestions.as_view(),name="view_suggestion"),
    url(r'^threshold_view/$',views.ThresholdView.as_view(),name="threshold"),
    url(r'^categorywise_list/(?P<categ>[-\w\b\w]+)/$',views.ViewCategoryWise.as_view(),name="category_wise"),
]