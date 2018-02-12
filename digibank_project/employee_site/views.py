from django.shortcuts import render

# Create your views here.
def empHome(request):
    return render(request,'employee_site/home.html',{})

def empLogin(request):
    return render(request, 'employee_site/login.html',{})

def emp_account_act(request):
    return render(request, "employee_site/emp_acc_act.html", {})

def emp_dd_req(request):
    return render(request, "employee_site/emp_dd_req.html", {})