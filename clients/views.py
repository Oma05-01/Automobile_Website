import datetime
from . models import Car, Client
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.sites.shortcuts import get_current_site
import random
import string
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Profile
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.


def client_home(request):

    # name = Client.objects.filter(client_name=icon)

    return render(request, 'client_Home.html',)


def client_login(request):

    if request.method == 'POST':

        user_ = request.POST.get('username')
        pass_ = request.POST.get('password')

        check_in = [user_, pass_]

        for it in check_in:
            if it != '':
                user = authenticate(username=user_, password=pass_)

                if user is not None and user.is_active:
                    login(request, user)
                    return redirect('CLhome')
                else:
                    # Return an 'invalid login' error message.
                    return render(request, 'login.html', {'error_message': 'Invalid login credentials'})
            else:
                msg = 'Please, ' + str(it) + ' should be filled'
                return render(request, 'Client_login.html', {'msg': msg})

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
            return render(request, 'error.html', {'error': error_message})

        if len(password1) < 8:
            msg = "Your password is too short"
            print('length')
            return render(request, 'error.html', {'msg': msg})

        if password1 != password2:
            msg = "Your passwords didn't match"
            print('match')
            return render(request, 'error.html', {'msg': msg})

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
            return render(request, 'error.html', {'msg': msg})

        # Create user without activation
        user = User.objects.create_user(username=username, email=email, password=password1, first_name=first_name, last_name=last_name)
        user.is_active = False  # Mark user as inactive until email is verified
        user.is_client = True
        user.save()
        print('created')

        # Send verification email
        send_verification_email(request, user)
        print('okay')

        # Redirect to a page informing the user to check their email
        return render(request, 'registration_pending.html')

    return render(request, 'Client_register.html')


def generate_verification_code():
    code = ''.join(random.choices(string.digits, k=6))
    return code


def send_verification_email(request, user):
    code = generate_verification_code()
    user.profile.verification_code = code  # Save the code in the user's profile
    user.profile.save()

    current_site = get_current_site(request)
    subject = 'Activate Your Account'
    message = render_to_string('verification_email.html', {
        'user': user,
        'domain': current_site.domain,
        'code': code,
    })
    plain_message = strip_tags(message)
    send_mail(subject, plain_message, 'from@example.com', [user.email], html_message=message)


def verify_code(request):
    if request.method == 'POST':
        verification_code = request.POST.get('verification_code')

        try:
            # Find the profile with the matching verification code
            profile = Profile.objects.get(verification_code=verification_code)

            # Retrieve the associated user
            user = profile.user

            # Ensure user is not already active
            if not user.is_active:
                # Activate the user
                user.is_active = True
                user.save()
                profile.is_verified = True
                profile.save()
                print('User verified and activated')
                return redirect('Client_login')  # Redirect to login page after verification

            else:
                # User is already active
                print('User is already active')

        except Profile.DoesNotExist:
            # Handle incorrect verification code scenario
            context = {'error_message': 'Incorrect verification code. Please try again.'}
            return render(request, 'error.html', context)

    # If the request method is not POST, render registration pending or another appropriate template
    return render(request, 'registration_pending.html')



def error_page(request):
    error_message = "Oops! Something went wrong."
    return render(request, 'error.html', {'error': error_message})


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


def new_post(request):

    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        name = request.POST.get('name')
        Desc = request.POST.get('description')

        date = datetime.datetime.now()
        day = date.day
        year = date.year
        month = date.month

        date1 = str(year) + '/' + str(month) + '/' + str(day)

        if name == "":
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

                    b = Car(Car_name=name, picname=filename, picurl=url, date=date1, Description=Desc)
                    b.save()

                    return redirect('Post_list')
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
            error = 'INVALID'
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



