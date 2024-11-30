from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from clients.models import Client
from Customers.models import Customer


def main(request):

    return render(request, 'home.html')


def profiles_exp(request):

    return render(request, 'profile_explanation.html')


def user_login(request):
    if request.method == "POST":
        # Get form data
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Log the user in
            login(request, user)

            # Check if the user is a Customer or Client
            try:
                customer_profile = Customer.objects.get(user=user)
                # Redirect to the customer dashboard
                return redirect('CUhome')  # Replace with your customer dashboard URL
            except Customer.DoesNotExist:
                pass  # Not a customer, continue to check client profile

            try:
                client_profile = Client.objects.get(user=user)
                # Redirect to the client dashboard
                return redirect('CLhome')  # Replace with your client dashboard URL
            except Client.DoesNotExist:
                pass  # Not a client, continue to check other profiles

            # If no profile is found, show an error
            messages.error(request, "You don't have a valid profile.")
            return redirect('login')  # Redirect to login page

        else:
            # Authentication failed
            messages.error(request, "Invalid username or password.")
            return redirect('login')  # Redirect to login page

    return render(request, 'login.html')  # Render the login form page
