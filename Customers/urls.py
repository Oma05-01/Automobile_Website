from django.urls import path
from . import views

urlpatterns = [
    path('home/<str:icon>', views.customer_home, name='home'),
    path('customer_login/', views.customer_login, name='mylogin'),
    path('customer_register/', views.customer_register, name='myregister'),
    path('customer_logout/', views.customer_logout, name='mylogout'),
    path('Customer_change_password/', views.customer_change_password, name='change_password'),
    path('Car-/<str:car>/', views.car_detail, name='item_detail'),
    path('search_car/<str:car>', views.search_car, name='search_car'),

]
