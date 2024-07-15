from django.urls import path
from . import views
from .views import client_verify_code

urlpatterns = [
    # path('home/<str:icon>', views.client_home, name='home'),
    path('client_home/', views.client_home, name='CLhome'),
    path('Client-Login/', views.client_login, name='Client_login'),
    path('client-register/', views.client_register, name='client_register'),
    path('client_verify/', client_verify_code, name='client_verify_code'),
    path('client_logout/', views.client_logout, name='Client_logout'),
    path('Client-Login/change_password/', views.client_change_password, name='change_password'),
    path('create_post/', views.new_post, name='New_Post'),
    path('car_list/', views.car_list, name='Car_listings'),
    path('edit_post/<int:pk>/', views.edit_post, name='Edit_post'),
    path('delete_post/<int:pk>/', views.delete_post, name='Delete_post'),
    path('check_username/', views.check_username, name='check_username'),
    path('check_email/', views.check_email, name='check_email'),
]
