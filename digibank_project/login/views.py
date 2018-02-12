from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import models
from _overlapped import NULL
from django.template.context_processors import request

# Create your views here.
def login(request):
    return render(request,'login/login.html',{})

