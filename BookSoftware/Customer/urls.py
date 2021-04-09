from django.conf.urls import url
from Customer import views

app_name="Customer"

urlpatterns=[
    url(r'^$',views.CustomerHomeView.as_view(),name="customer_home"),
    url(r'^search_book/(?P<query>[-\w\s]+)/$',views.BookSearchView,name="search_book"),
    url(r'^book_details/(?P<pk>\d+)/$',views.BookDetailView.as_view(),name="detail_book"),
    url(r'^add_wishlist/$',views.AddWishlistView,name="add_wishlist"),
    url(r'^wishlist_view/(?P<user>[-\w]+)/$',views.WishlistView.as_view(),name="list_wish"),
    url(r'^wishlist_changes/$',views.DeleteWishList,name="delete_wishlist"),
    url(r'^cart/(?P<user>[-\w]+)/$', views.CartView.as_view(), name="view_cart"),
    url(r'^cart_changes/$',views.ChangeCart,name="cart_change"),
    url(r'^change_quantity/$',views.ChangeQuantityView,name="change_quantity"),
    url(r'^add_address/$',views.AddAddressView,name="address_add"),
    url(r'^order_placed/$',views.SuccessOrderView,name="order_success"),
    url(r'^view_transactions/$',views.TransactionView,name="view_transaction"),
    url(r'^suggest/$',views.SuggestView,name="suggest"),
    url(r'^suggest_next/$',views.SuccessSuggest,name="suggest_success"),



]