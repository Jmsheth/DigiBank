from django.shortcuts import render, redirect
from customer_site.models import Customer
from core_files.models import DDRequest
from .forms import EmpAccActivation, EmpAccActivationSearch
from .models import EmpDetail


# Create your views here.
def empHome(request):
    try:
        employee= EmpDetail.objects.get(userid=request.session['empsession'])
        return render(request,'employee_site/home.html',{'empsession':request.session['empsession'],'employee':employee})
    except:
        request.session['empsession']=""
        return render(request, 'employee_site/home.html', {'empsession': request.session['empsession']})

def empLogin(request):
    return render(request,'employee_site/login.html',{})

def auth(request):
    userid= request.POST['userid']
    password=request.POST['password']
    try:
        emp = EmpDetail.objects.get(userid=userid,password=password)
        request.session['empsession']= emp.userid
        return redirect('employee_site:empHome')
    except:
        return redirect({'employee_site:empLogin'})

def empLogout(request):
    try:
        del request.session['empsession']
    except KeyError:
        pass
    return redirect('employee_site:empHome')


def emp_account_act(request, pk=-1):
    form = EmpAccActivationSearch()
    if request.method == "GET":
        if "search" in request.GET:
            firstName = request.GET["f_name"]
            lastName = request.GET["l_name"]
            userid = request.GET["u_name"]
            idNumber = request.GET["id_num"]
            customer_list = Customer.objects.all()
            if firstName:
                print(firstName)
                customer_list = customer_list.filter(firstName=firstName)
            if lastName:
                print(lastName)
                customer_list = customer_list.filter(lastName=lastName)
            if userid:
                print(userid)
                customer_list = customer_list.filter(userid=userid)
            if idNumber:
                print(idNumber)
                customer_list = customer_list.filter(idNumber=idNumber)
            print(customer_list)
        else:
            customer_list = Customer.objects.all()
        print("search button pressed")
        return render(request,
                      "employee_site/emp_acc_act.html",
                      {"customers": customer_list,
                       "form": form})
    if request.method == "POST":
        # modify the account
        print("activate/deactivate pressed")
        print(request.POST)
        customer = Customer.objects.get(pk=pk)
        customer.active = not customer.active
        customer.save()
        return redirect("/employee/account_activation/")


def emp_dd_req(request):
    dd_requests = DDRequest.objects.filter(approved=False)
    return render(request,
                  "employee_site/emp_dd_req.html",
                  {"dd_requests": dd_requests})
