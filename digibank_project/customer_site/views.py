from django.shortcuts import render, redirect
from django.http import HttpResponse
from . models import Customer
from _overlapped import NULL
from django.template.context_processors import request

# Create your views here.
def login(request):
    return render(request,'login/login.html',{})


def auth(request):
    userid = request.POST["loginid"]
    password = request.POST["pwd"]

    user = Customer.objects.get(userid=userid, password=password)
    if user is not None:
        return redirect('homepage:index')
        print("Success Login")
    else:
        return redirect('customer_site:login')


def forget(request):
    return render(request, 'login/forget.html', {})


def reset(request):
    email = request.POST["email"]
    idnum = request.POST["idnum"]

    found = Customer.objects.get(emailAdd=email, idNumber=idnum)
    if found is not None:
        global em
        em = email
        return redirect('login:resetpassword')
    else:
        ...


def resetpassword(request):
    return render(request, 'login/reset.html', {})


def resetauth(request):
    pwd1 = request.POST["pwd1"]
    pwd2 = request.POST["pwd2"]

    if pwd1 == pwd2:
        Customer.objects.filter(emailAdd=em).update(password=pwd1)
        return redirect('login:login')
    else:
        print("password not match")
