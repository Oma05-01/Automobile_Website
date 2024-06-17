from django.urls import path
from . import views

urlpatterns = [
    path('home/<str:icon>', views.client_home, name='home'),
    path('Client-Login', views.client_login, name='Client_login'),
    path('register/', views.client_register, name='Client_register'),
    path('logout/', views.client_logout, name='Client_logout'),
    path('Client-Login/change_password/', views.client_change_password, name='change_password'),
    path('create_post/', views.new_post, name='New_Post'),
    path('edit_post/<int:pk>/', views.edit_post, name='Edit_post'),
    path('delete_post/<int:pk>/', views.delete_post, name='Delete_post'),
]
