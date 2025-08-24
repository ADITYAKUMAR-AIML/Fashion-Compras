from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup_page, name='signup_page'),
    path('login/', views.login_page, name='login_page'),
    path('logout/', views.Logout, name='logout'),
    path('Cart-items/', views.Cart, name='cart'),
    path('deals/', views.Deals, name='deals'),
    path('Item/', views.Item, name='item'),
    path('Contact/', views.Contact, name='Contact'),
]
