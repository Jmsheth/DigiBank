from django.shortcuts import render, redirect
from customer_site.models import Customer
from core_files.models import DDRequest, CheckRequest, Account
from .forms import EmpAccActivationSearch,NewCustomer
from .models import EmpDetail
from core_files.models import Account,Transactions
from django.views.generic import CreateView
from django.utils import timezone
import datetime
from datetime import timedelta


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
        return redirect('employee_site:empLogin')

def empLogout(request):
    try:
        del request.session['empsession']
    except KeyError:
        pass
    return redirect('employee_site:empHome')

def forgotpass(request):
    return render(request,'employee_site/forgot.html',{})

def reset(request):

    try:
        emp = EmpDetail.objects.get(emailAdd=request.POST["email"],empId=request.POST["idnum"])
        if emp is not None:
            global user
            user = emp.userid
            return redirect('employee_site:resetpassword')
    except:
        return redirect('employee_site:forgot')

def resetpassword(request):
    return render(request,'employee_site/reset.html',{})

def resetauth(request):
    try:
        if request.POST['pwd1']==request.POST['pwd2']:
            print("match")
            print(user)
            EmpDetail.objects.filter(userid=user).update(password=request.POST['pwd2'])
            print("update")
            return redirect('employee_site:empHome')
    except:
        return redirect('employee_site:reset')

def newCustomer(request):
    if request.session['empsession'] is not "":
        print("this",request.session['empsession'],"is")
        return render(request,'employee_site/newcustomer.html',{'empsession': request.session['empsession']})
    else:
        return redirect('employee_site:empHome')

def newaccCustomer(request):
    pwd1 = request.POST['pwd1']
    pwd2 = request.POST['pwd2']
    global user
    user = request.POST['userid']
    if(pwd1==pwd2):
        customer = Customer()
        customer.firstName=request.POST['firstName']
        customer.middleName = request.POST['middleName']
        customer.lastName = request.POST['lastName']
        customer.address = request.POST['address']
        customer.city = request.POST['city']
        customer.state = request.POST['state']
        customer.zipCode = request.POST['zipCode']
        customer.country = request.POST['country']
        customer.phoneNumber = request.POST['phoneNumber']
        customer.emailAdd = request.POST['emailAdd']
        customer.kycId = request.POST['idtype']
        customer.idNumber = request.POST['kycId']
        customer.userid = user
        customer.password = pwd1
        customer.save()
        return redirect('employee_site:newaccount')

def newaccount(request):
        return render(request,'employee_site/newacccustomer.html',{'empsession': request.session['empsession']})

def addAccDetail(request):
    cust=Customer.objects.get(userid=user)
    print(cust.id)
    account = Account()
    account.accountNum= request.POST['accountNum']
    account.routingNum=request.POST['routingNum']
    account.acntType=request.POST['acntType']
    account.balance=request.POST['balance']
    account.owner=cust
    account.save()
    return redirect('employee_site:empHome')

def emp_account_act(request, pk=-1):
    try:
        request.session["empsession"]
    except:
        return redirect("employee_site:empHome")
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
                customer_list = customer_list.filter(firstName__iexact=firstName)
            if lastName:
                print(lastName)
                customer_list = customer_list.filter(lastName__iexact=lastName)
            if userid:
                print(userid)
                customer_list = customer_list.filter(userid__iexact=userid)
            if idNumber:
                print(idNumber)
                customer_list = customer_list.filter(idNumber=idNumber)
            print(customer_list)
        else:
            customer_list = Customer.objects.all()
        print("search button pressed")
        return render(request,
                      "employee_site/emp_acc_act.html",
                      {"empsession": request.session['empsession'],
                       "customers": customer_list,
                       "form": form})
    if request.method == "POST":
        # modify the account
        print("activate/deactivate pressed")
        print(request.POST)
        customer = Customer.objects.get(pk=pk)
        customer.active = not customer.active
        customer.save()
        return redirect("/employee/account_activation/")


def emp_dd_req(request, pk=-1):
    try:
        request.session["empsession"]
    except:
        return redirect("employee_site:empHome")

    dd_requests = DDRequest.objects.filter(approved=False)
    if not dd_requests or len(dd_requests) == 0:
        return redirect("/employee/")
    if pk == -1:
        dd_req = dd_requests[0]
    else:
        dd_req = DDRequest.objects.get(pk=pk)
    customer = Customer.objects.get(pk=dd_req.requester_id)
    if request.method == "GET":
        return render(request,
                      "employee_site/emp_dd_req.html",
                      {"empsession": request.session['empsession'],
                       "dd_requests": dd_requests,
                       "dd_req": dd_req,
                       "customer": customer})
    if request.method == "POST":
        dd_req.approved = True
        dd_req.save()
        return redirect('employee_site:DD Requests')


def emp_checks(request, pk=-1):
    try:
        request.session["empsession"]
    except:
        return redirect("employee_site:empHome")

    check_requests = CheckRequest.objects.filter(approved=False)
    if pk != -1:
        check_req = CheckRequest.objects.get(pk=pk)
    else:
        if len(check_requests) == 0:
            return redirect("employee_site:empHome")
        check_req = check_requests[0]
    acc = Account.objects.get(pk=check_req.account_id)
    customer = Customer.objects.get(pk=acc.owner_id)
    if request.method == "GET":
        return render(request,
                      "employee_site/emp_check.html",
                      {
                       'empsession': request.session['empsession'],
                       "check_requests": check_requests,
                       "check_req": check_req,
                       "customer": customer,
                       "acc": acc})
    if request.method == "POST":
        check_req.approved = not check_req.approved
        check_req.save()
        return redirect("/employee/check_req/")

def empAccountSummary(request):
    if request.session['empsession'] is not "":
        employee = EmpDetail.objects.get(userid=request.session['empsession'])
        account = Account.objects.all()
        return render(request,'EmpAccount/AccountSummary.html',{'empsession':request.session['empsession'],'account':account,'employee':employee})
    else:
        return redirect('employee_site:empHome')

def authEmpAccountdetails(request):
    try:
        # print("Inside")
        accnum = request.POST['accnum']
        # print("This is ",accnum)
        acc = Account.objects.get(accountNum=accnum)
        # print(acc)
        return render(request, 'EmpAccount/displaydetails.html',{'empsession': request.session['empsession'], 'acc': acc})
    except:
        return redirect('employee_site:empHome')



def empTransactionReport(request):
    if request.session['empsession'] is not "":
        employee = EmpDetail.objects.get(userid=request.session['empsession'])
        account = Account.objects.all()
        return render(request, 'EmpAccount/TxnReport.html',
                  {'empsession': request.session['empsession'], 'account': account,'employee':employee})
    else:
        return redirect('employee_site:empHome')

def authEmpReportdetails(request):
    try:
        print("Inside")
        accnum = request.POST['accnum']
        print("This is ",accnum)

        dateFrom = request.POST['fromdate']
        print("This is ", dateFrom)
        dateTo = request.POST['todate']

        new_date = datetime.datetime.strptime(dateTo,'%Y-%m-%d')
        final_date=new_date+datetime.timedelta(days=2)

       # print("This is ",  dateTo+ datetime.timedelta(days=1))
        accntFromAccount = Account.objects.get(accountNum=accnum)
        print("This is ", accntFromAccount)
        txnCr = Transactions.objects.filter(accntFrom=accntFromAccount).filter(dateTime__range=[dateFrom,final_date])
        txnDb = Transactions.objects.filter(accntTo=accnum).filter(dateTime__range=[dateFrom,final_date])
        return render(request, 'EmpAccount/displayTxndetails.html', {'empsession': request.session['empsession'], 'txnDb': txnDb,'txnCr': txnCr})
    except:
        return redirect('employee_site:empHome')
