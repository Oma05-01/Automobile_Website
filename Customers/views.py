import datetime
from .models import Customer
from clients.models import Car
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.sites.shortcuts import get_current_site
import random
import string
from datetime import date
from django.http import JsonResponse
from .models import CustomerProfile
from Admins.models import Dates
import json
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
# Create your views here.


def customer_home(request):

    # person = Customer.objects.filter(customer_name=icon)

    return render(request, 'Customer_Home.html')


def customer_login(request):
    if request.method == 'POST':

        user_ = request.POST.get('username')
        pass_ = request.POST.get('password')

        check_in = [user_, pass_]

        for it in check_in:
            if it != '':
                user = authenticate(username=user_, password=pass_)

                if user is not None and user.is_active:
                    login(request, user)
                    return redirect('CUhome')
                else:
                    # Return an 'invalid login' error message.
                    return render(request, 'error.html', {'error_message': 'Invalid login credentials'})
            else:
                msg = 'Please, ' + str(it) + ' should be filled'
                return render(request, 'Customer_login.html', {'msg': msg})
    return render(request, 'Customer_login.html')


def customer_register(request):
    if request.method == "POST":
        # Get form data
        first_name = request.POST.get('First_name')
        last_name = request.POST.get('Last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Validate form data
        if not all([first_name, last_name, username, email, phone_number, password1, password2]):
            error_message = 'All fields are required'
            print('field')
            return JsonResponse({'status': 'error', 'msg': error_message})

        if User.objects.filter(username=username).exists():
            msg = "This username is already taken UVuTu.!MyY#b5yB"
            return JsonResponse({'status': 'error', 'msg': msg})
        #
        # if User.objects.filter(email=email).exists():
        #     msg = "This email is already registered"
        #     return JsonResponse({'status': 'error', 'msg': msg})

        if len(password1) < 8:
            msg = "Your password is too short"
            print('length')
            return JsonResponse({'status': 'error', 'msg': msg})

        if password1 != password2:
            msg = "Your passwords didn't match"
            print('match')
            return JsonResponse({'status': 'error', 'msg': msg})

        # Check password strength
        count1 = count2 = count3 = count4 = 0
        for i in password1:
            if '0' <= i <= '9':
                count1 = 1
            if 'A' <= i <= 'Z':
                count2 = 1
            if 'a' <= i <= 'z':
                count3 = 1
            if '!' <= i <= '(':
                count4 = 1

        if not all([count1, count2, count3, count4]):
            msg = "Your password isn't strong enough"
            print('here')
            return JsonResponse({'status': 'error', 'msg': msg})

        # Create user without activation
        user = User.objects.create_user(username=username, email=email, password=password1, first_name=first_name,
                                        last_name=last_name)
        user.is_active = False
        user.save()
        print('created')

        customer = Customer.objects.create(user=user, First_name=first_name, Last_name=last_name, email=email,
                                           phone_number=phone_number, is_customer=True, username=username)

        customer.save()

        # Send verification email
        send_verification_email(request, user)
        print('okay')

        # Redirect to a page informing the user to check their email
        return render(request, 'customer_registration_pending.html')

    return render(request, 'Customer_register.html')


def check_username(request):
    username = request.GET.get('username')
    is_taken = User.objects.filter(username=username).exists()
    return JsonResponse({'is_taken': is_taken})


def check_email(request):
    email = request.GET.get('email')
    is_taken = User.objects.filter(email=email).exists()
    return JsonResponse({'is_taken': is_taken})


def generate_verification_code():
    code = ''.join(random.choices(string.digits, k=6))
    return code


def send_verification_email(request, user):
    code = generate_verification_code()

    if hasattr(user, 'customer_profile'):
        profile = user.customer_profile
    else:
        print("error")
        raise AttributeError('User has no profile associated')

    profile.verification_code = code
    profile.save()

    current_site = get_current_site(request)
    subject = 'Activate Your Account'
    message = render_to_string('verification_email.html', {
        'user': user,
        'domain': current_site.domain,
        'code': code,
    })
    plain_message = strip_tags(message)
    send_mail(subject, plain_message, 'from@example.com', [user.email], html_message=message)


def customer_verify_code(request):
    if request.method == 'POST':
        verification_code = request.POST.get('verification_code')

        try:
            # Find the profile with the matching verification code
            profile = CustomerProfile.objects.get(verification_code=verification_code)

            # Retrieve the associated user
            user = profile.user

            # Ensure user is not already active
            if not user.is_active:
                # Activate the user
                user.is_active = True
                user.save()
                profile.is_verified = True
                profile.save()
                return redirect('customer_login')  # Redirect to login page after verification
            else:
                # User is already active
                context = {'error_message': 'User is already active.'}
                return render(request, 'error.html', context)

        except CustomerProfile.DoesNotExist:
            # Handle incorrect verification code scenario
            context = {'error_message': 'Incorrect verification code. Please try again.'}
            print('here')
            return render(request, 'error.html', context)

    # If the request method is not POST, render registration pending or another appropriate template
    return render(request, 'customer_verify.html')


def error_page(request):
    error_message = "Oops! Something went wrong."
    return render(request, 'error.html', {'error': error_message})


def customer_logout(request):

    logout(request)

    return redirect('Customer_login')


def customer_change_password(request):

    if not request.user.is_authenticated:
        return redirect('mylogin')

    if request.method == "POST":

        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        if pass1 == "" or pass2 == "":
            error = "Both fields Required"
            print(request.user)
            return render(request, 'back/error.html', {'error': error})

        user = authenticate(username=request.user, password=pass1)

        if user:
            if len(pass2) < 6:
                error = "Your password must be greater than six characters"
                return render(request, 'back/error.html', {'error': error})

            count1 = 0
            count2 = 0
            count3 = 0
            count4 = 0

            for i in pass2:
                if '0' <= i <= '9':
                    count1 = 1
                if 'A' <= i <= 'Z':
                    count2 = 1
                if 'a' <= i <= 'z':
                    count3 = 1
                if '!' <= i <= '(':
                    count4 = 1

            if count1 and count2 and count3 and count4 == 1:

                user = User.objects.get(username=request.user)
                user.set_password(pass2)
                user.save()
                return redirect('mylogout')

        else:
            error = "INCORRECT PASSWORD"
            return render(request, 'back/error.html', {'error': error})

    return render(request, 'Customer_Home.html')


def car_detail(request, car):

    item = Car.objects.all(Car_name=car)

    return render(request, '', {'item': item})


def schedule_date(request):

    unavailable_dates = list(Dates.objects.values_list('Scheduled_date', flat=True))
    unavailable_dates_json = json.dumps([d.isoformat() for d in unavailable_dates])
    return render(request, 'schedule_date.html', {'unavailable_dates': unavailable_dates_json})


def search_car(request, car):

    if request.method == "POST":
        searched_car = request.POST.get('searched')
        seen_car = Car.objects.filter(Car_name__contains=searched_car)
    else:
        return render(request, '')

    return render(request, '', {'searched': searched_car, 'seen_cars': seen_car})



