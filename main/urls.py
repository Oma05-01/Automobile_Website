from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main_page'),
    path('signup/profile-explanation/', views.profiles_exp, name='profile-explanation'),
    path('login/', views.user_login, name='login'),

]
