from django.shortcuts import render
from customer_site.models import Customer
from core_files.models import DDRequest


# Create your views here.
def empHome(request):
    return render(request,'employee_site/home.html',{})

def empLogin(request):
    return render(request, 'employee_site/login.html',{})

def emp_account_act(request):
    customer_list = Customer.objects.all()
    return render(request,
                  "employee_site/emp_acc_act.html",
                  {"customers": customer_list})


def emp_dd_req(request):
    dd_requests = DDRequest.objects.filter(approved=False)
    return render(request,
                  "employee_site/emp_dd_req.html",
                  {"dd_requests": dd_requests})
