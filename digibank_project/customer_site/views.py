from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.http import HttpResponse
from . models import Customer,Account,Transaction
from .forms import userAccountSummary,userTransactionReport,userFundstransfer
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
        #return redirect('customer_site:forgot')


def resetpassword(request):
    return render(request, 'login/reset.html', {})


def resetauth(request):
    pwd1 = request.POST["pwd1"]
    pwd2 = request.POST["pwd2"]

    if pwd1 == pwd2:
        Customer.objects.filter(emailAdd=em).update(password=pwd1)
        return redirect('login:login')
    else:
        return redirect('customer_site:resetpassword')


class userAccountSummary_vw(CreateView):
    model = Account
    template_name = 'AccountSummary.html'
    form_class = userAccountSummary

    def form_valid(self, form):
        if form.is_valid():
            uAcntSmry = form.save(commit=False)
            return super(userAccountSummary_vw,self).form_valid(form)

    def edit_vw(request,id):

        instance = Account.objects.get(id=id)
        form = userAccountSummary(request.POST or None,instance=instance)
        if form.is_valid():
            form.save()
            return redirect("edit")
        return render(request,'AccountSummary.html',{'form':form})

#
# class userTransactionReport_vw(CreateView):
#     model = Account
#     template_name = 'FundsTransfr.html'
#     form_class = userTransactionReport
#
#     def form_valid(self, form):
#         if form.is_valid():
#             utrxnSmry = form.save(commit=False)
#             return super(userTransactionReport_vw,self).form_valid(form)
#
#
#      def edit_vw(request,id):
#
#         instance = Account.objects.get(id=id)
#         form = userTransactionReport(request.POST or None,instance=instance)
#         if form.is_valid():
#             form.save()
#             return redirect("FundsTransfr.html")
#         return render(request,'/',{'form':form})
#
#
# class userFundsTransfer_vw(CreateView):
#     model = Account
#     template_name = 'TxnReport.html'
#     form_class = userFundstransfer
#
#     def form_valid(self, form):
#         if form.is_valid():
#             uTrsfr = form.save(commit=False)
#             return super(userFundsTransfer_vw,self).form_valid(form)
#
#
#     def edit_vw(request,id):
#
#         instance = Account.objects.get(id=id)
#         form = userFundstransfer(request.POST or None,instance=instance)
#         if form.is_valid():
#             form.save()
#             return redirect("edit")
#         return render(request,'TxnReport.html',{'form':form})