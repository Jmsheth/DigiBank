from django import forms
from django import forms
from core_files.models import Account


class EmpDDRequestForm(forms.BaseForm):
    pass


class EmpAccActivationSearch(forms.Form):
    f_name = forms.CharField(label="First name:",
                             required=False)
    l_name = forms.CharField(label="Last Name:",
                             required=False)
    u_name = forms.CharField(label="Username",
                             required=False)
    id_num = forms.IntegerField(label="ID Number:",
                                 required=False)


class EmpAccActivation(forms.ModelForm):
    class Meta:
        fields = ["active"]

class userAccountSummary(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('owner', 'accountNum', 'acntType')


class userTransactionReport(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('owner','accountNum', 'acntType',)


class userFundsTransfer(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('accountNum', 'routingNum','owner')