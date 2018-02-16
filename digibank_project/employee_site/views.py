from django.shortcuts import render, redirect
from customer_site.models import Customer
from core_files.models import DDRequest, CheckRequest, Account
from .forms import EmpAccActivationSearch,NewCustomer
from .models import EmpDetail
from core_files.models import Account
from django.views.generic import CreateView


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


def emp_dd_req(request, pk=-1):
    dd_requests = DDRequest.objects.filter(approved=False)
    if not dd_requests:
        redirect("/employee/")
    if pk == -1:
        dd_req = dd_requests[0]
    else:
        dd_req = DDRequest.objects.get(pk=pk)
    customer = Customer.objects.get(pk=dd_req.requester_id)
    if request.method == "GET":
        return render(request,
                      "employee_site/emp_dd_req.html",
                      {"dd_requests": dd_requests,
                       "dd_req": dd_req,
                       "customer": customer})
    if request.method == "POST":
        dd_req.approved = True
        dd_req.save()
        return redirect("/employee/dd_req/")


def emp_checks(request, pk=-1):
    check_requests = CheckRequest.objects.filter(approved=False)
    if pk != -1:
        check_req = CheckRequest.objects.get(pk=pk)
    else:
        check_req = check_requests[0]
    acc = Account.objects.get(pk=check_req.account_id)
    customer = Customer.objects.get(pk=acc.owner_id)
    if request.method == "GET":
        return render(request,
                      "employee_site/emp_check.html",
                      {"check_requests": check_requests,
                       "check_req": check_req,
                       "customer": customer,
                       "acc": acc})
    if request.method == "POST":
        check_req.approved = not check_req.approved
        check_req.save()
        return redirect("/employee/check_req/")

def empAccountSummary(request):
    customer = Customer.objects.get(userid=request.session['sessionid'])
    cid = customer.id
    # print(customer)
    # print(cid)
    account = Account.objects.filter(owner_id=cid)
    # print(account)

    return render(request,'EmpAccount/AccountSummary.html',
                  {'sessionid':request.session['sessionid'],'account':account,'customer':customer})

def authEmpAccountdetails(request):
    try:
        # print("Inside")
        accnum = request.POST['accnum']
        # print("This is ",accnum)
        acc = Account.objects.get(accountNum=accnum)
        # print(acc)
        return render(request, 'EmpAccount/displaydetails.html',{'sessionid': request.session['sessionid'], 'acc': acc})
    except:
        return redirect('employee_site:empHome')



def empTransactionReport(request):
    customer = Customer.objects.get(userid=request.session['sessionid'])
    cid = customer.id
    # print(customer)
    # print(cid)
    account = Account.objects.filter(owner_id=cid)


    return render(request, 'EmpAccount/TxnReport.html',
                  {'sessionid': request.session['sessionid'], 'account': account,'customer': customer})


def authEmpReportdetails(request):
    try:
        print("Inside")
        accnum = request.POST['accnum']
        print("This is ",accnum)
        txnCr = Transactions.objects.filter(accntFrom=accnum)
        txnDb = Transactions.objects.filter(accntTo=accnum)
        print("Here")
        print("This is",txnDb)
        print("This is", txnCr)
        return render(request, 'EmpAccount/displayTxndetails.html', {'sessionid': request.session['sessionid'], 'txnDb': txnDb,'txnCr': txnCr})
    except:
        return redirect('employee_site:empHome')

