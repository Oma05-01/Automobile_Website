from django.urls import path
from . import views
from .views import customer_verify_code


urlpatterns = [
    path('customer_home/', views.customer_home, name='CUhome'),
    path('customer_login/', views.customer_login, name='customer_login'),
    path('customer_register/', views.customer_register, name='customer_register'),
    path('customer_logout/', views.customer_logout, name='mylogout'),
    path('customer_login/change_password/', views.customer_change_password, name='change_password'),
    path('Car-/<str:car>/', views.car_detail, name='item_detail'),
    path('search_car/<str:car>', views.search_car, name='search_car'),
    path('error/', views.error_page, name='error'),
    path('schedule-date/', views.schedule_date, name='schedule_date'),
    path('check_email/', views.check_email, name='check_email'),
    path('customer_verify/', customer_verify_code, name='customer_verify_code'),

]
