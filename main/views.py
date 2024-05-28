
from django.shortcuts import render, get_object_or_404, redirect
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render


def myregister(request):

    if request.method == "POST":

        name = request.POST.get('name')
        username = request.POST.get('uname')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if name == "":
            msg = "Name field must be filled"
            return render(request, 'front/msgbox.html', {'msg': msg})

        print(username, email, password1, password2)

        if password1 != password2:
            msg = "Your passwords didn't match"
            return render(request, 'front/msgbox.html', {'msg': msg})

        count1 = 0
        count2 = 0
        count3 = 0
        count4 = 0

        for i in password1:
            if '0' <= i <= '9':
                count1 = 1
            if 'A' <= i <= 'Z':
                count2 = 1
            if 'a' <= i <= 'z':
                count3 = 1
            if '!' <= i <= '(':
                count4 = 1

        if len(password1) < 8:
            msg = "Your password is too short"
            return redirect(request, 'front/msgbox.html', {'msg': msg})

        if count1 == 0 or count2 == 0 or count3 == 0 or count4 == 0:
            msg = "Your password isn't strong enough"
            return render(request, 'front/msgbox.html', {'msg': msg})

        if len(User.objects.filter(username=username)) == 0 and len(User.objects.filter(email=email)) == 0:

            user = User.objects.create_user(username=name, email=email, password=password1)
            b = user
            b.save()

    return render(request, 'front/login.html')

def mylogin(request):

    if request.method == 'POST':

        utxt = request.POST.get('username')
        ptxt = request.POST.get('password')

        if utxt != '' and ptxt != '':

            user = authenticate(username=utxt, password=ptxt)

            if user:
                login(request, user)
                return redirect('home')

    return render(request, 'front/login.html')

def mylogout(request):

    logout(request)

    return redirect('mylogin')