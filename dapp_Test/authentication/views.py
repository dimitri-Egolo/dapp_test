# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic.edit import CreateView
# Create your views here.

def index(request):
    return render(request, 'authentication/login.html', {})


def register(request):
    return render(request, 'authentication/register.html', {})


def login(request):
    return render(request, 'authentication/register.html', {})


def logout(request):
    return render(request, 'authentication/register.html', {})
