from django.shortcuts import render, redirect
from django.http import HttpResponse
from . models import Customer
from core_files.models import Account
from django.views.generic import CreateView

from _overlapped import NULL
from django.template.context_processors import request
from .forms import userAccountSummary, userFundsTransfer, userTransactionReport

# Create your views here.
def home(request):
    #return render(request, 'login/cusHome.html')
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
    print("Reset Area")
    try:
        if(newpass==conpass):
            Customer.objects.filter(userid=request.session['sessionid'], password=currpass).update(password=conpass)
        del request.session['sessionid']
        return redirect('login:cusHome')
    except:
        return redirect('login:changePass')

def logout(request):
    try:
        del request.session['sessionid']
    except KeyError:
        pass
    return redirect('login:cusHome')


class userAccountSummary_vw(CreateView):
    model = Account
    template_name = 'UserAccount/AccountSummary.html'
    form_class = userAccountSummary

    def form_valid(self, form):
        if form.is_valid():
            utrxnSmry = form.save(commit=False)
            return super(userAccountSummary_vw,self).form_valid(form)

    # def form_valid(self, form):
    #     instance = Account.objects.get(id=id)
    #     form = userAccountSummary(request.POST or None,instance=instance)
    #     if form.is_valid():
    #         uTrsfr = form.save(commit=False)
    #         return super(userFundsTransfer_vw,self).form_valid(form)
    #         form.save()
    #         return redirect("edit")
    #     return render(request,'UserAccount/AccountSummary.html',{'form':form})

#
class userTransactionReport_vw(CreateView):
    model = Account
    template_name = 'UserAccount/TxnReport.html'
    form_class = userTransactionReport

    def form_valid(self, form):
        if form.is_valid():
            utrxnSmry = form.save(commit=False)
            return super(userTransactionReport_vw,self).form_valid(form)


class userFundsTransfer_vw(CreateView):
    model = Account
    template_name = 'UserAccount/FundsTransfr.html'
    form_class = userFundsTransfer

    def form_valid(self, form):
        if form.is_valid():
            uTrsfr = form.save(commit=False)
            return super(userFundsTransfer_vw,self).form_valid(form)



