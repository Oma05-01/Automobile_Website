from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.shortcuts import render


def main(request):

    return render(request, 'home.html')