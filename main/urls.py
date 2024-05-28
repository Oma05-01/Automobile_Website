from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.mylogin, name='mylogin'),
    path('register/', views.myregister, name='myregister'),
    path('logout/', views.mylogout, name='mylogout'),
    path('panel/change_password/', views.change_password, name='change_password'),
]
