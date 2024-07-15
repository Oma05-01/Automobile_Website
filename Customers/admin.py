from django.contrib import admin
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages

from .models import Customer


@admin.action(description='Delete selected users and their corresponding customer')
def delete_users_and_customer(modeladmin, request, queryset):
    for user in queryset:
        try:
            customer = Customer.objects.get(username=user.username)
            customer.delete()
            user.delete()
            messages.success(request, f'Successfully deleted user and Customer: {user.username}')
        except ObjectDoesNotExist:
            messages.warning(request, f'Customer with user {user.username} does not exist.')
        except Exception as e:
            messages.error(request, f'Error deleting user {user.username}: {e}')


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('First_name', 'Last_name', 'username', 'email', 'phone_number', 'date_created', 'is_customer')
    search_fields = ('First_name', 'Last_name', 'username', 'email')


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    actions = [delete_users_and_customer]


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
