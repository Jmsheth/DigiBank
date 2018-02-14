from django.shortcuts import render, redirect
from customer_site.models import Customer
from core_files.models import DDRequest, CheckRequest, Account
from .forms import EmpAccActivation, EmpAccActivationSearch
from django.shortcuts import render,redirect
from ..customer_site.models import Customer
from ..core_files.models import DDRequest, Account
from django.views.generic import CreateView
from ..employee_site.forms import empFundsTransfer, empAccountSummary, empTransactionReport


# Create your views here.
def empHome(request):
    return render(request,'employee_site/home.html',{})


def empLogin(request):
    return render(request, 'employee_site/login.html',{})


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



class empAccountSummary_vw(CreateView):
    model = Account
    template_name = 'UserAccount/AccountSummary.html'
    form_class = empAccountSummary

    def form_valid(self, form):
        if form.is_valid():
            utrxnSmry = form.save(commit=False)
            return super(empAccountSummary_vw,self).form_valid(form)

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
class empTransactionReport_vw(CreateView):
    model = Account
    template_name = 'UserAccount/TxnReport.html'
    form_class = empTransactionReport

    def form_valid(self, form):
        if form.is_valid():
            utrxnSmry = form.save(commit=False)
            return super(empTransactionReport_vw,self).form_valid(form)



#
#
#




