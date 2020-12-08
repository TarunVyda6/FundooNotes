from __future__ import absolute_import

from django.shortcuts import render, redirect
from rest_framework.viewsets import ModelViewSet
from .models import NewUser
from fundooapp.serializers import UserDetailsSerializer
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout


class UserDetailsCrud(ModelViewSet):
    queryset = NewUser.objects.all()
    serializer_class = UserDetailsSerializer


def register_page(request):
    """
    this function takes request as input and register the details, if all the details are valid then redirect to login page
    """
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('user_name')
            messages.success(request, 'Account was created for ' + user)
            return redirect('login')

    context = {'form': form}
    print("failed")

    return render(request, 'fundooapp/Register.html',
                  context)


def login_page(request):
    """
    takes request as input and if valid credentials are provided then it will redirect to home page
    """
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or password is incorrect')

    context = {}
    return render(request, 'fundooapp/Login.html',
                  context)


def home_page(request):
    """
    takes request as input parameter and displays home page
    :rtype: object
    """
    context = {}
    return render(request, 'fundooapp/Home.html',
                  context)


def logout_page(request):
    """
    takes request as input parameter and if the account is logged out then it will redirect to login page
    """
    logout(request)
    return redirect('login')
