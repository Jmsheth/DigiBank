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




