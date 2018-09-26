# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from authentication.models import UserProfile
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.views import generic
# Create your views here.

def index(request):
    return render(request, 'authentication/login.html', {})


def register(request):
    return render(request, 'authentication/register.html', {})


def createAccount(request):
    UserProfile.objects.create_user(first_name=request.POST['first_name'],
                                    last_name=request.POST['last_name'],
                                    username=request.POST['username'],
                                    email=request.POST['email'],
                                    password=request.POST['password'],
                                    photo=request.POST['photo'])
    return HttpResponseRedirect(reverse('auth:authentication'))


def loginView(request):
    email = request.POST['email']
    pwd = request.POST['password']
    user = authenticate(email=email, password=pwd)

    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect(reverse('home'))
        else:
            return render(request, 'authentication/login.html', {
            'error_message': "This account has been disabled.",
            'status': "Unauthorized"
        })
    else:
        return render(request, 'authentication/login.html', {
            'error_message': "User does not exist.",
        })


@login_required
def logoutView(request):
    logout(request)
    return render(request, 'authentication/login.html', {})


class DetailView(generic.DetailView):
    model = UserProfile
    template_name = 'authentication/detailUser.html'


@login_required
def updateUser(request, pk):
    user_to_update = get_object_or_404(UserProfile, pk=pk)
    print(request.POST)
    if user_to_update != request.user:
        """i have to update this later. it must return a message saying that
        user does not have rights to do this operation.
        """
        return HttpResponseRedirect(reverse('home'))
    else:
        user_to_update.first_name = request.POST['first_name']
        user_to_update.last_name = request.POST['last_name']
        user_to_update.username = request.POST['username']
        user_to_update.email = request.POST['email']
        user_to_update.photo = request.POST['photo']
        if request.POST['change_pwd'] == 'on':
            user_to_update.set_password(request.POST['password'])
        user_to_update.save()
        return HttpResponseRedirect(reverse('home'))
