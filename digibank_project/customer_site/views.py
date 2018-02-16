from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import Customer
from core_files.models import Account, CheckRequest, DDRequest
from _overlapped import NULL
from django.template.context_processors import request
from core_files.models import Account,Transactions
from django.views.generic import CreateView
from .forms import userTransactionReport,userFundsTransfer,userAccountSummary
from django.utils import timezone
import datetime
from datetime import timedelta
# Create your views here.
def home(request):
    try:
        customer = Customer.objects.get(userid=request.session['sessionid'])
        return render(request, 'login/cusHome.html', {'sessionid': request.session['sessionid'],'customer':customer})
    except:
        request.session['sessionid'] = ""
        return render(request, 'login/cusHome.html', {'sessionid': request.session['sessionid']})

def login(request):
    return render(request,'login/login.html',{})


def auth(request):
    userid = request.POST["loginid"]
    password = request.POST["pwd"]
    try:
        user = Customer.objects.get(userid=userid,password=password)
        request.session['sessionid'] = user.userid
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
    return render(request,'login/changepass.html',{'sessionid':request.session['sessionid']})


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
    currpass = request.POST["curpass"]
    newpass = request.POST["newpass"]
    conpass = request.POST["conpass"]

    try:
        if(newpass==conpass):
            Customer.objects.filter(userid={'sessionid':request.session['sessionid']}, password=currpass).update(password=conpass)

        del request.session['sessionid']
        return redirect('login:cusHome') #{'sessionid': request.session['sessionid']})

    except:
        return redirect('login:changePass')

def logout(request):
    try:
        del request.session['sessionid']
    except KeyError:
        pass
    return redirect('login:cusHome')

# def userAccountSummary(request):
#     pass

def updateprofile(request):
    customer = Customer.objects.get(userid=request.session['sessionid'])
    return render(request, 'login/editprofile.html',{'sessionid':request.session['sessionid'], "customer": customer})

def updateauth(request):
    try:
        Customer.objects.filter(userid=request.session['sessionid']).update(firstName=request.POST['firstName'],
                            middleName=request.POST['middleName'],lastName=request.POST['lastName'],
                            address=request.POST['address'],city=request.POST['city'],state=request.POST['state'],
                            country=request.POST['country'],zipCode=request.POST['zipCode'],phoneNumber=request.POST['phoneNumber'],
                            emailAdd=request.POST['emailAdd'],userid=request.POST['userid'])
        return redirect('login:cusHome')
    except:
        return redirect('login:updateprofile')


def userAccountSummary(request):
    customer = Customer.objects.get(userid=request.session['sessionid'])
    cid = customer.id
    # print(customer)
    # print(cid)
    account = Account.objects.filter(owner_id=cid)
    # print(account)

    return render(request,'UserAccount/AccountSummary.html',
                  {'sessionid':request.session['sessionid'],'account':account,'customer':customer})

def authdetails(request):
    try:
        # print("Inside")
        accnum = request.POST['accnum']
        userid= request.POST['userid']
        #print(accnum)
        # print("This is ",accnum)
        if 'all' in accnum:
            #print(userid)
            acc = Account.objects.filter(owner_id=userid)
            new_acc=acc
        else:

            acc = Account.objects.get(accountNum=accnum)
            new_acc=[acc]
        return render(request, 'UserAccount/displaydetails.html',{'sessionid': request.session['sessionid'], 'acc': new_acc})
    except:
        ...


def userTransactionReport(request):
    customer = Customer.objects.get(userid=request.session['sessionid'])
    cid = customer.id
    # print(customer)
    # print(cid)
    account = Account.objects.filter(owner_id=cid)


    return render(request, 'UserAccount/TxnReport.html',
                  {'sessionid': request.session['sessionid'], 'account': account,'customer': customer})


def authReportdetails(request):
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
        # txnCr = Transactions.objects.filter(accntFrom=accntFromAccount)
        # txnDb = Transactions.objects.filter(accntTo=accnum)

        print("Here")
        print("This is",txnDb)
        print("This is", txnCr)
        return render(request, 'UserAccount/displayTxndetails.html', {'sessionid': request.session['sessionid'], 'txnDb': txnDb,'txnCr': txnCr})
    except:
        ...


def userFundsTransfer(request):
        customer = Customer.objects.get(userid=request.session['sessionid'])
        cid = customer.id
        account = Account.objects.filter(owner_id=cid)

        return render(request, 'UserAccount/FundsTransfr.html',
                      {'sessionid': request.session['sessionid'], 'account': account, 'customer': customer})

def authFundTrsfrDetails(request):
    try:
        print("Inside")
        accnum = request.POST['accnum']
        print("This is ", accnum)
        fromroutingNo = request.POST['fromroutingNo']
        print("This is ", fromroutingNo)
        toAccount = request.POST['toAccount']
        print("This is ", toAccount)
        toroutingNo = request.POST['toroutingNo']
        print("This is ", toroutingNo)
        amount = request.POST['amount']
        print("This is ", amount)
        transferDesc = request.POST['transferDesc']
        print("This is ", transferDesc)
        txn = Transactions()
        txn.accntFrom = Account.objects.get(accountNum=accnum)
        txn.accntTo = toAccount
        txn.toRoutingNo = toroutingNo
        txn.amount = amount
        txn.transferDesc = transferDesc
        txn.save()

        return render(request, 'UserAccount/displayFundsTrnsfrDtls.html',
                      {'sessionid': request.session['sessionid'], 'txn': txn})

    except Exception as e:
        print(e)
        return redirect("/userTransactionReport/")


def user_dd_req(request):
    if request.method == "GET":
        user = Customer.objects.get(
            userid=request.session["sessionid"])
        accounts = Account.objects.filter(owner_id=user.id)
        return render(request,
                      "customer_site/user_dd_req.html",
                      {"user": user,
                       "accounts": accounts})
    if request.method == "POST":
        dd_req = DDRequest()
        dd_req.rec_name = request.POST["rec_name"]
        dd_req.amount = request.POST["amount"]
        dd_req.address_st = request.POST["address_st"]
        dd_req.address_city = request.POST["address_city"]
        dd_req.address_state = request.POST["address_state"]
        dd_req.address_zip = request.POST["address_zip"]
        dd_req.rec_phone = request.POST["rec_phone"]
        dd_req.payable_date = request.POST["payable_date"]
        dd_req.message = request.POST["message"]
        dd_req.requester = Customer.objects.get(
            userid=request.session["sessionid"])
        dd_req.send_date = request.POST["send_date"]
        dd_req.account_from = Account.objects.get(
            pk=request.POST["account_from"]
        )
        if not dd_req.save():
            return redirect("login:cusHome")
        else:
            messages.info(request, "Unable to store data.")
            return redirect("/dd_request/")


def user_check_req(request):
    if request.method == "GET":
        user = Customer.objects.get(userid=request.session["sessionid"])
        accounts = Account.objects.filter(owner_id=user.id)
        return render(request,
                      "customer_site/user_check_request.html",
                      {"user": user,
                       "accounts": accounts})
    if request.method == "POST":
        print(request.POST)
        check_req = CheckRequest()
        check_req.address_st = request.POST["address_st"]
        check_req.address_city = request.POST["address_city"]
        check_req.address_state = request.POST["address_state"]
        check_req.address_zip = request.POST["address_zip"]
        check_req.account = Account.objects.get(
            pk=request.POST["account_id"])
        if not check_req.save():
            return redirect("login:cusHome")
        else:
            messages.info(request, "Unable to store data.")
            return redirect("/request_checks/")
