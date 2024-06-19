from .models import Customer
from clients.models import Car
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from .utils import generate_verification_token
# Create your views here.


def customer_home(request, icon):

    person = Customer.objects.filter(customer_name=icon)

    return render(request, 'Customer_Home.html', {'customer': person})


def customer_login(request):
    if request.method == 'POST':

        user_ = request.POST.get('username')
        pass_ = request.POST.get('password')

        check_in = [user_, pass_]

        for it in check_in:
            if it != '':
                user = authenticate(username=user_, password=pass_)

                if user:
                    login(request, user)
                    return redirect('home')
            else:
                msg = 'Please, ' + str(it) + ' should be filled'
                return render(request, 'Customer_login.html', {'msg': msg})
    return render(request, 'Customer_login.html')


def customer_register(request):

    if request.method == "POST":
        First_name = request.method.POST.get('First_name')
        Last_name = request.method.POST.get('First_name')
        username = request.method.POST.get('First_name')
        email = request.method.POST.get('First_name')
        phone_number = request.method.POST.get('First_name')
        date_created = request.method.POST.get('First_name')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        details = [First_name, Last_name, email, phone_number, date_created, password1, password2]

        for detes in details:
            if detes == "":
                error_message = 'The ' + str(detes) + " field is required"
                return render(request, """this is supposed to be a pop up message""", {'error': error_message})

        if len(password1) < 8:
            msg = "Your password is too short"
            return render(request, '', {'msg': msg})

        if password1 != password2:
            msg = "Your passwords didn't match"
            return render(request, '', {'msg': msg})

        count1 = 0; count2 = 0; count3 = 0; count4 = 0
        check = [count1, count2, count3, count4]

        for i in password1:
            if '0' <= i <= '9':
                count1 = 1
            if 'A' <= i <= 'Z':
                count2 = 1
            if 'a' <= i <= 'z':
                count3 = 1
            if '!' <= i <= '(':
                count4 = 1

        for i in check:
            if i == 0:
                msg = "Your password isn't strong enough"
                return render(request, '', {'msg': msg})

        if len(User.objects.filter(username=username)) == 0 and len(User.objects.filter(email=email)) == 0:

            b = User.objects.create_user(username=username, email=email, password=password1)
            b.save()

    return redirect('login.html')


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

    return render(request, 'Client_Home.html')


def car_detail(request, car):

    item = Car.objects.all(Car_name=car)

    return render(request, '', {'item': item})


def search_car(request, car):

    if request.method == "POST":
        searched_car = request.POST.get('searched')
        seen_car = Car.objects.filter(Car_name__contains=searched_car)
    else:
        return render(request, '')

    return render(request, '', {'searched': searched_car, 'seen_cars': seen_car})


def verify_email(request, token):
    User = get_user_model()
    try:
        profile = User.profile.objects.get(verification_token=token)
        profile.user.is_active = True
        profile.user.save()
        # Optional: Clear verification token or mark the email as verified
        profile.verification_token = ''
        profile.save()
        return render(request, 'verification_success.html')
    except User.profile.DoesNotExist:
        return render(request, 'verification_failure.html')
