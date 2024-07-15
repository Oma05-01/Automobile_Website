import datetime
from . models import Car, Client
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.sites.shortcuts import get_current_site
import random
import string
from django.shortcuts import render, redirect
from .models import ClientProfile
from django.http import JsonResponse
from django.contrib.auth import get_user_model

# Create your views here.


def client_home(request):

    return render(request, 'client_Home.html')
    # name = Client.objects.filter(client_name=icon)


def client_login(request):

    if request.method == 'POST':

        user_ = request.POST.get('username')
        pass_ = request.POST.get('password')

        check_in = [user_, pass_]

        for it in check_in:
            if it != '':
                user = authenticate(username=user_, password=pass_)

                check_client = Client.objects.get(username=user_).username
                print(user_)
                print(check_client)
                if user.username == check_client:
                    login(request, user)
                    print('user is client')
                    return redirect('CLhome')
                else:
                    # Return an 'invalid login' error message.
                    return render(request, 'login.html', {'error_message': 'Invalid login credentials'})
            else:
                msg = 'Please, ' + str(it) + ' should be filled'
                return JsonResponse({'status': 'error', 'msg': msg})

    return render(request, 'client_login.html')


def client_register(request):
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

        client = Client.objects.create(user=user, First_name=first_name, Last_name=last_name, email=email,
                                       phone_number=phone_number, is_client=True, username=username)

        client.save()

        # Send verification email
        send_verification_email(request, user)
        print('done')

        # Redirect to a page informing the user to check their email
        return render(request, 'client_registration_pending.html')

    return render(request, 'Client_register.html')


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

    if hasattr(user, 'client_profile'):
        profile = user.client_profile
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


def client_logout(request):
    logout(request)

    return render(request, 'Client_Home.html')


def client_change_password(request):
    if not request.user.is_authenticated:
        return redirect('mylogin')

    if request.method == "POST":

        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        if pass1 == "" or pass2 == "":
            error = "Both fields Required"
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


def new_post(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        name = request.POST.get('name')
        Desc = request.POST.get('description')
        available_for_testing = request.POST.get('available_for_testing')
        test_location = request.POST.get('test_location')
        price = float(request.POST.get('price'))

        date = datetime.datetime.now()
        day = date.day
        year = date.year
        month = date.month

        date1 = f"{year}/{month}/{day}"

        if not name or not Desc or not available_for_testing:
            error = 'All Fields Required'
            return render(request, 'back/error.html', {'error': error})

        try:
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            url = fs.url(filename)

            if str(myfile.content_type).startswith('image'):
                if myfile.size < 500000000:
                    b = Car(
                        Car_name=name,
                        pic_name=str(filename),
                        picurl=str(url),
                        date=date1,
                        Description=Desc,
                        Available_for_testing=available_for_testing,
                        test_location=test_location,
                        price=price
                    )
                    b.save()
                    return redirect('Car_listings')
                else:
                    fs.delete(filename)
                    error = 'Your file is bigger than 5MB'
                    print(error)
                    return render(request, 'back/error.html', {'error': error})
            else:
                fs.delete(filename)
                error = 'Your file is not supported'
                print(error)
                return render(request, 'back/error.html', {'error': error})

        except Exception as e:
            error = f'INVALID: {str(e)}'
            print(e)
            return render(request, 'back/error.html', {'error': error})

    return render(request, 'New_post.html')


def edit_post(request, pk):

    if not request.user.is_authenticated:
        return redirect('login')

    if len(Car.objects.filter(pk=pk)) == 0:
        error = 'Car Not Found'
        return render(request, 'back/error.html', {'error': error})

    car_ = Car.objects.get(pk=pk)

    if request.method == 'POST':
        name = request.POST.get('name')
        desc = request.POST.get('description')

        if name == "" or desc == "":
            error = 'All Fields Required'
            # for error to show in the html page, it needs to be placed in a dict {'error': error}
            return render(request, 'back/error.html', {'error': error})

        try:
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            url = fs.url(filename)

            if str(myfile.content_type).startswith('image'):

                if myfile.size < 5000000:

                    b = Car.objects.get(pk=pk)

                    fss = FileSystemStorage()
                    fss.delete(b.picname)

                    b.Car_name = name
                    b.Description = desc
                    b.picname = filename
                    b.picurl = url

                    b.save()

                    return redirect('car_list')
                else:
                    fs = FileSystemStorage()
                    fs.delete(myfile)

                    error = 'Your file Is Bigger Than 5Mb'
                    return render(request, 'back/error.html', {'error': error})
            else:
                fs = FileSystemStorage()
                fs.delete(filename)

                error = 'Your file Is Not Supported'
                return render(request, 'back/error.html', {'error': error})

        except:

            b = Car.objects.get(pk=pk)

            b.Car_name = name
            b.Description = desc

            b.save()

            return redirect('car_list')

    return render(request, 'Edit_post.html')


def delete_post(request, pk):

    if not request.user.is_authenticated:
        return redirect('login')

    try:
        b = Car.objects.get(pk=pk)

        fs = FileSystemStorage()
        fs.delete(b.picname)

        b.delete()

    except:
        error = 'Something wrong'
        return render(request, 'back/error.html', {'error': error})

    return redirect('news_list')


def car_list(request):

    return render(request, 'car_list.html')


def client_verify_code(request):
    if request.method == 'POST':
        verification_code = request.POST.get('verification_code')

        try:
            # Find the profile with the matching verification code
            profile = ClientProfile.objects.get(verification_code=verification_code)
            print('nawa')
            print(profile)

            # Retrieve the associated user
            user = profile.user

            # Ensure user is not already active
            if not user.is_active:
                # Activate the user
                user.is_active = True
                user.save()
                profile.is_verified = True
                profile.save()
                print('yes?')
                return redirect('Client_login')  # Redirect to login page after verification
            else:
                # User is already active
                context = {'error_message': 'User is already active.'}
                return render(request, 'error.html', context)

        except ClientProfile.DoesNotExist:
            # Handle incorrect verification code scenario
            context = {'error_message': 'Incorrect verification code. Please try again.'}
            return render(request, 'error.html', context)

    # If the request method is not POST, render registration pending or another appropriate template
    return render(request, 'client_verify.html')
