from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup_page, name='signup_page'),
    path('login/', views.login_page, name='login_page'),
    path('logout/', views.Logout, name='logout'),
    path('Cart-items/', views.Cart, name='cart'),
    path('deals/', views.Deals, name='deals'),
    path('Item/id=pk', views.Item, name='item'),
    path("add/", views.add_item, name="add_item"),
    path('Contact/', views.Contact, name='Contact'),
    path('PrivacyPolicy/', views.PrivacyPolicy, name='PrivacyPolicy'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
