from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request,'employee_site/home.html')

def login(request):
    return render(request,'employee_site/login.html')