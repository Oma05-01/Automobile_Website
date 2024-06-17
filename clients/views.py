import datetime
from . models import Car, Client
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


# Create your views here.


def client_home(request, icon):

    name = Client.objects.filter(client_name=icon)

    return render(request, 'Client_Home.html', {'client': name })


def client_login(request):

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

    return render(request, 'Client_Home.html')


def client_register(request):

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

    return render(request, 'Client_Home.html')


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

