# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from authentication.models import UserProfile
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.core.files.storage import FileSystemStorage
# Create your views here.

def index(request):
    return render(request, 'authentication/login.html', context={'message': ''})


def register(request):
    return render(request, 'authentication/register.html', context={'message': ''})


def createAccount(request):
    try:
        user1 = UserProfile.objects.create_user(first_name=request.POST.get('first_name', None),
                                                last_name=request.POST.get('last_name', None),
                                                username=request.POST['username'],
                                                email=request.POST['email'],
                                                password=request.POST['password'])
        if request.FILES['photo']:
            photo = request.FILES['photo']
            fs = FileSystemStorage()
            filename = fs.save(photo.name, photo)
            uploaded_file_url = fs.url(filename)
            user1.photo = uploaded_file_url
            user1.save()
        return HttpResponseRedirect(reverse('auth:authentication'))
    except KeyError:
        # redisplay register form to fill in required fields
        return render(request, 'authentication/register.html', context={'message': 'Please fill the form!'})


def loginView(request):
    email = request.POST.get('email', None)
    pwd = request.POST.get('password', None)
    user = authenticate(email=email, password=pwd)

    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect(reverse('home'))
        else:
            return render(request, 'authentication/login.html', context={
            'message': "This account has been disabled.",
            'status': "Unauthorized"})
    else:
        return render(request,
                      'authentication/login.html',
                      context={'message': "This user does not exist."})


@login_required
def logoutView(request):
    logout(request)
    return render(request, 'authentication/login.html', {'message': ''})


class DetailView(generic.DetailView):
    model = UserProfile
    template_name = 'authentication/detailUser.html'
    context={'color': "black"}


@login_required
def updateUser(request, pk):
    user_to_update = get_object_or_404(UserProfile, pk=pk)
    if user_to_update != request.user:
        """i have to update this later. it must return a message saying that
        user does not have rights to do this operation.
        """
        return HttpResponseRedirect(reverse('home'))
    else:
        user_to_update.first_name = request.POST.get('first_name', None)
        user_to_update.last_name = request.POST.get('last_name', None)
        try:
            user_to_update.username = request.POST['username']
            user_to_update.email = request.POST['email']
        except:
            render(request, 'authentication/detailUser.html', {'message': 'Please fill in the required fields!'})

        if 'photo' in request.FILES:
            fs = FileSystemStorage()
            filename = fs.save(photo.name, photo)
            uploaded_file_url = fs.url(filename)
            user_to_update.photo = uploaded_file_url

        password = request.POST.get('password', None)
        if password and password != '':
            user_to_update.set_password(password)
        user_to_update.save()
        return HttpResponseRedirect(reverse('home'))
