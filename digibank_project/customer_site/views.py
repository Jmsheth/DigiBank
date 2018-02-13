from django.shortcuts import render, redirect
from django.http import HttpResponse
from . models import Customer
from _overlapped import NULL
from django.template.context_processors import request

# Create your views here.
def home(request):
    try:
        return render(request,'login/cusHome.html',{'sessionid':request.session['sessionid']})
    except:
        request.session['sessionid'] = ""
        return render(request, 'login/cusHome.html', {'sessionid': request.session['sessionid']})

def login(request):
    return render(request,'login/login.html',{})


def auth(request):
    userid = request.POST["loginid"]
    password = request.POST["pwd"]
    try:
        user = Customer.objects.get(userid=userid, password=password)
        if user is not None:
            request.session['sessionid'] = str(user)
            return redirect('login:cusHome')
    except:
        return redirect('login:login')


def forget(request):
    return render(request, 'login/forget.html', {})


def reset(request):
    email = request.POST["email"]
    idnum = request.POST["idnum"]
    try:
        found = Customer.objects.get(emailAdd=email, idNumber=idnum)
        if found is not None:
            global em
            em = email
            return redirect('login:resetpassword')
    except:
        return redirect('login:forgot')


def resetpassword(request):
    return render(request, 'login/reset.html', {})

def changepass(request):
    return render(request,'login/changepass.html',{})


def resetauth(request):
    pwd1 = request.POST["pwd1"]
    pwd2 = request.POST["pwd2"]

    try:
        if pwd1 == pwd2:
            Customer.objects.filter(emailAdd=em).update(password=pwd1)
            return redirect('login:login')
    except:
        return redirect('login:resetpassword')

def resetpassauth(request):
    return render(request,'login/changepass.html',{})


def userAccountSummary(request):
    ...
